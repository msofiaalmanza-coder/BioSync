from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class VistaBienvenida(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("Vista/bienvenida.ui", self)

        self.setWindowTitle("BioMed Analyzer")