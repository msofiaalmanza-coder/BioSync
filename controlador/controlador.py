from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
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

    def validar_login(self):

        usuario = self.login.txtUsuario.text()
        password = self.login.txtPassword.text()
        resultado = self.modelo_db.validar_usuario(
            usuario,
            password
        )

        if resultado:

            self.login.hide()

            self.principal.show()

            self.principal.txtUsuarioSesion.setText(
                resultado[1]
            )

            self.principal.txtRolSesion_2.setText(
                resultado[2]
            )

            self.login.lblMensaje.setText("")

        else:

            self.login.lblMensaje.setText(
                "Usuario o contraseña incorrectos"
            )
