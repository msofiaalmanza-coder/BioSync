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
        self.main = uic.loadUi(
            "vista/main.ui"
        )

        self.login = uic.loadUi(
            "vista/login.ui"
        )

        self.principal = uic.loadUi(
            "vista/principal.ui"
        )

        self.modelo_db = ModeloDB()
        self.modelo_dicom = DicomModel()
        self.modelo_senales = SenalesModel()
        self.modelo_tabular = ModeloTabular()

        self.id_usuario_actual = None

        self.conectar_eventos()
        print("cargado")

    def conectar_eventos(self):
        self.main.btnIngresar.clicked.connect(
            self.abrir_login
        )

        self.main.btnSalir.clicked.connect(
            self.cerrar_app
        )


        self.login.btnLogin.clicked.connect(
            self.validar_login
        )

        self.login.btnVolver.clicked.connect(
            self.volver_main
        )

        self.principal.btnCapturarFoto.clicked.connect(
            self.capturar_foto
        )

        self.principal.btnCargarDicom.clicked.connect(
            self.cargar_dicom
        )

        self.principal.btnConvertirNifti.clicked.connect(
            self.convertir_nifti
        )

        self.principal.btnGuardarCSV.clicked.connect(
            self.guardar_csv
        )

        self.principal.btnZoom.clicked.connect(
            self.aplicar_zoom
        )

        self.principal.btnGuardarRecorte.clicked.connect(
            self.guardar_recorte
        )

        self.principal.btnSegmentar.clicked.connect(
            self.segmentar_imagen
        )

        self.principal.btnMorfologia.clicked.connect(
            self.aplicar_morfologia
        )

        self.principal.btnCargarMat.clicked.connect(
            self.cargar_mat
        )

        self.principal.btnAgregarRuido.clicked.connect(
            self.agregar_ruido
        )

        self.principal.btnMostrarCanales.clicked.connect(
            self.mostrar_canales
        )

        self.principal.btnEstadisticas.clicked.connect(
            self.mostrar_estadisticas
        )

        self.principal.btnCargarDatos.clicked.connect(
            self.cargar_datos
        )

        self.principal.btnGraficar.clicked.connect(
            self.graficar_columna
        )

        self.principal.btnScatter.clicked.connect(
            self.graficar_scatter
        )

        self.principal.pushButton.clicked.connect(
            self.cerrar_app
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
        try:
            self.modelo_db.cerrar()
        except:
            pass

        self.main.close()
        self.login.close()
        self.principal.close()

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
        print("Foto")

    def cargar_dicom(self):
        print("DICOM")

    def convertir_nifti(self):
        print("NIFTI")

    def guardar_csv(self):
        print("CSV")


    def aplicar_zoom(self):
        print("ZOOM")

    def guardar_recorte(self):
        print("RECORTE")

    def segmentar_imagen(self):
        print("SEGMENTACION")

    def aplicar_morfologia(self):
        print("MORFOLOGIA")

    def cargar_mat(self):
        print("MAT")

    def agregar_ruido(self):
        print("RUIDO")

    def mostrar_canales(self):
        print("CANALES")

    def mostrar_estadisticas(self):
        print("ESTADISTICAS")

    def cargar_datos(self):
        print("DATOS")

    def graficar_columna(self):
        print("GRAFICA")

    def graficar_scatter(self):
        print("SCATTER")
