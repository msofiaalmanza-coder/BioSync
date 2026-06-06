from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QTableWidgetItem
)
from PyQt5.QtGui import QPixmap

import cv2
import os
from datetime import datetime

from modelo.modelo_db import ModeloDB
from modelo.modelo_dicom import DicomModel
from modelo.modelo_señales import SenalesModel
from modelo.modelo_tabular import ModeloTabular


class Controlador:

    def __init__(self):

        self.main = uic.loadUi("vista/main.ui")
        self.login = uic.loadUi("vista/login.ui")
        self.principal = uic.loadUi("vista/principal.ui")

        self.modelo_db = ModeloDB()
        self.modelo_dicom = DicomModel()
        self.modelo_senales = SenalesModel()
        self.modelo_tabular = ModeloTabular()

        self.id_usuario_actual = None

        self.conectar_eventos()

    def conectar_eventos(self):

        # MAIN

        self.main.btnIngresar.clicked.connect(
            self.abrir_login
        )

        self.main.btnSalir.clicked.connect(
            self.cerrar_app
        )

        # LOGIN

        self.login.btnLogin.clicked.connect(
            self.validar_login
        )

        self.login.btnVolver.clicked.connect(
            self.volver_main
        )

        # INICIO

        self.principal.btnCapturarFoto.clicked.connect(
            self.capturar_foto
        )

        # DICOM

        self.principal.btnCargarDicom.clicked.connect(
            self.cargar_dicom
        )

        self.principal.btnConvertirNifti.clicked.connect(
            self.convertir_nifti
        )

        self.principal.btnGuardarCSV.clicked.connect(
            self.guardar_csv
        )

    def mostrar_main(self):

        self.main.show()

    def abrir_login(self):

        self.main.hide()
        self.login.show()

    def volver_main(self):

        self.login.hide()
        self.main.show()

    def cerrar_app(self):

        self.modelo_db.cerrar()
        self.main.close()

    def validar_login(self):

        usuario = self.login.txtUsuario.text()
        password = self.login.txtPassword.text()

        resultado = self.modelo_db.validar_usuario(
            usuario,
            password
        )

        if resultado:

            self.id_usuario_actual = resultado[0]

            self.principal.txtUsuarioSesion.setText(
                str(resultado[1])
            )

            self.principal.txtRolSesion_2.setText(
                str(resultado[2])
            )

            self.principal.txtFechaSesion.setText(
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

            self.login.hide()
            self.principal.show()

        else:

            self.login.lblMensaje.setText(
                "Usuario o contraseña incorrectos"
            )

    def capturar_foto(self):

        if self.id_usuario_actual is None:
            return

        if not os.path.exists("fotos"):
            os.makedirs("fotos")

        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        cap.release()

        if not ret:

            QMessageBox.warning(
                self.principal,
                "Error",
                "No se pudo acceder a la cámara"
            )

            return

        ruta = (
            f"fotos/usuario_"
            f"{self.id_usuario_actual}.jpg"
        )

        cv2.imwrite(
            ruta,
            frame
        )

        self.modelo_db.guardar_sesion(
            self.id_usuario_actual,
            ruta
        )

        pixmap = QPixmap(ruta)

        self.principal.lblFotoUsuario.setPixmap(
            pixmap
        )

        self.principal.lblFotoUsuario.setScaledContents(
            True
        )

        QMessageBox.information(
            self.principal,
            "Foto",
            "Foto capturada correctamente"
        )

    def cargar_dicom(self):

        carpeta = QFileDialog.getExistingDirectory(
            self.principal,
            "Seleccione carpeta DICOM"
        )

        if not carpeta:
            return

        try:

            self.modelo_dicom.cargar_dicom(
                carpeta
            )

            metadata = (
                self.modelo_dicom.metadata_para_tabla()
            )

            self.principal.tableMetadatos.setRowCount(
                len(metadata)
            )

            self.principal.tableMetadatos.setColumnCount(
                2
            )

            for fila, dato in enumerate(metadata):

                self.principal.tableMetadatos.setItem(
                    fila,
                    0,
                    QTableWidgetItem(
                        str(dato[0])
                    )
                )

                self.principal.tableMetadatos.setItem(
                    fila,
                    1,
                    QTableWidgetItem(
                        str(dato[1])
                    )
                )

            dimensiones = (
                self.modelo_dicom.dimensiones()
            )

            self.principal.sliderAxial.setMaximum(
                dimensiones[0] - 1
            )

            self.principal.sliderCoronal.setMaximum(
                dimensiones[1] - 1
            )

            self.principal.sliderSagital.setMaximum(
                dimensiones[2] - 1
            )

            QMessageBox.information(
                self.principal,
                "DICOM",
                "Estudio cargado correctamente"
            )

        except Exception as e:

            QMessageBox.warning(
                self.principal,
                "Error",
                str(e)
            )

    def convertir_nifti(self):

        ruta, _ = QFileDialog.getSaveFileName(
            self.principal,
            "Guardar NIFTI",
            "",
            "NIFTI (*.nii)"
        )

        if not ruta:
            return

        try:

            self.modelo_dicom.convertir_nifti(
                ruta
            )

            QMessageBox.information(
                self.principal,
                "NIFTI",
                "Conversión realizada"
            )

        except Exception as e:

            QMessageBox.warning(
                self.principal,
                "Error",
                str(e)
            )

    def guardar_csv(self):

        ruta, _ = QFileDialog.getSaveFileName(
            self.principal,
            "Guardar CSV",
            "",
            "CSV (*.csv)"
        )

        if not ruta:
            return

        try:

            self.modelo_dicom.guardar_csv(
                ruta
            )

            QMessageBox.information(
                self.principal,
                "CSV",
                "Archivo guardado"
            )

        except Exception as e:

            QMessageBox.warning(
                self.principal,
                "Error",
                str(e)
            )
