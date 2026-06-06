from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class VistaLogin(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("login.ui", self)

        self.setWindowTitle("Login")