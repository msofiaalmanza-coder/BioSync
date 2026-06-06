from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class VistaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("Vista/principal.ui", self)

        self.setWindowTitle("BioSync")

        self.inicializar()

    def inicializar(self):

        if hasattr(self, "txtUsuarioSesion"):
            self.txtUsuarioSesion.setText("")

        if hasattr(self, "txtRolSesion_2"):
            self.txtRolSesion_2.setText("")

        if hasattr(self, "txtFechaSesion"):
            self.txtFechaSesion.setText("")

        if hasattr(self, "sliderAxial"):
            self.sliderAxial.setValue(0)

        if hasattr(self, "sliderCoronal"):
            self.sliderCoronal.setValue(0)

        if hasattr(self, "sliderSagital"):
            self.sliderSagital.setValue(0)

        if hasattr(self, "spinKernel"):
            self.spinKernel.setValue(3)

        if hasattr(self, "comboSegmentacion"):

            self.comboSegmentacion.clear()

            self.comboSegmentacion.addItems([
                "binary",
                "binary_inv",
                "trunc",
                "tozero",
                "tozero_inv"
            ])

        if hasattr(self, "comboMorfologia"):

            self.comboMorfologia.clear()

            self.comboMorfologia.addItems([
                "erosion",
                "dilatacion",
                "apertura",
                "cierre",
                "gradiente"
            ])