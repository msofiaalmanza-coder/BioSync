from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class VistaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista/login.ui", self)
        self.btn_ingresar.clicked.connect(self.ingresar)
        self.callback = None

    def ingresar(self):
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()
        if self.callback:
            self.callback(usuario, contrasena)

    def mostrar_error(self, msg):
        self.lbl_error.setText(msg)