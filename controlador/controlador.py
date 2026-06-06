from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from modelo.modelo_db import ModeloDB
from modelo.modelo_dicom import DicomModel
from modelo.modelo_señales import SenalesModel
from modelo.modelo_tabular import ModeloTabular


class Controlador:

    def _init_(self):

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

        self.conectar_eventos()

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
