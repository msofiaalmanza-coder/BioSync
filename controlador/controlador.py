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

    # =====================================
    # EVENTOS
    # =====================================

    def conectar_eventos(self):
        print("entre")

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
        self.principal.btnCapturarFoto.clicked.connect(
            lambda: print("Foto")
        )

        self.principal.btnCargarDicom.clicked.connect(
            lambda: print("DICOM")
        )

        self.principal.btnConvertirNifti.clicked.connect(
            lambda: print("NIFTI")
        )

        self.principal.btnGuardarCSV.clicked.connect(
            lambda: print("CSV")
        )

    # =====================================
    # NAVEGACION
    # =====================================

    def mostrar_main(self):

        self.main.show()

    def abrir_login(self):

        self.main.hide()
        self.login.show()

    def volver_main(self):

        self.login.hide()
        self.main.show()

    def cerrar_app(self):

        self.main.close()
    print("Conectando")
    # =====================================
    # LOGIN
    # =====================================

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

    # =====================================
    # FOTO
    # =====================================

    def capturar_foto(self):

        pass

    # =====================================
    # DICOM
    # =====================================

    def cargar_dicom(self):

        pass

    def convertir_nifti(self):

        pass

    def guardar_csv(self):

        pass