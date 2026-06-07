
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap


class MainView(QMainWindow):
    """
    Vista de la pantalla de inicio de BioSync.

    Señales:
        sig_entrar: emitida cuando el usuario hace clic en 'Entrar'.
        sig_salir:  emitida cuando el usuario hace clic en 'Salir'.
    """

    sig_entrar = pyqtSignal()
    sig_salir  = pyqtSignal()



    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window()
        self._build_ui()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("BioSync")
        self.setMinimumSize(770, 583)
        self.resize(785, 630)

    def _build_ui(self):
      
        central = QWidget(self)
        self.setCentralWidget(central)

        grid = QGridLayout(central)


        self.frame1 = QFrame()
        self.frame1.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.frame1.setFrameShape(QFrame.StyledPanel)
        self.frame1.setFrameShadow(QFrame.Raised)
        grid.addWidget(self.frame1, 0, 0)


        self.lblLogo = QLabel(self.frame1)
        self.lblLogo.setGeometry(290, 20, 191, 171)
        self.lblLogo.setScaledContents(True)
        self.lblLogo.setPixmap(QPixmap("logogood.png"))

        self.lblTitulo = QLabel(self.frame1)
        self.lblTitulo.setGeometry(200, 190, 381, 81)
        self.lblTitulo.setStyleSheet('font: 75 20pt "Times New Roman";')
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setText(
            '<html><body><p align="center">'
            '<span style=" font-size:26pt; font-weight:600;">BioSync</span>'
            '</p></body></html>'
        )

 
        self.lblSubtitulo = QLabel(self.frame1)
        self.lblSubtitulo.setGeometry(20, 190, 770, 211)
        self.lblSubtitulo.setStyleSheet('font: italic 10pt "Times New Roman";')
        self.lblSubtitulo.setAlignment(Qt.AlignCenter)
        self.lblSubtitulo.setText(
            '<html><body><p align="center">'
            '<span style=" font-size:14pt;">Bienvenido al sistema de análisis biomédico</span>'
            '</p></body></html>'
        )


        self.btnIngresar = QPushButton("Entrar", self.frame1)
        self.btnIngresar.setGeometry(310, 360, 171, 81)
        self.btnIngresar.setStyleSheet(
            'font: 75 12pt "Times New Roman";'
            'border-color: rgb(0, 0, 0);'
            'background-color: rgb(240, 240, 240);'
        )

        self.btnSalir = QPushButton("Salir", self.frame1)
        self.btnSalir.setGeometry(310, 470, 171, 81)
        self.btnSalir.setStyleSheet(
            'font: 75 12pt "Times New Roman";'
            'background-color: rgb(240, 240, 240);'
        )

    def _connect_signals(self):
        """Conecta los widgets con las señales de la vista."""
        self.btnIngresar.clicked.connect(self.sig_entrar)
        self.btnSalir.clicked.connect(self.sig_salir)

    def set_logo(self, pixmap: QPixmap):

        self.lblLogo.setPixmap(pixmap)

    def set_titulo(self, texto: str):

        self.lblTitulo.setText(texto)

    def set_subtitulo(self, texto: str):

        self.lblSubtitulo.setText(texto)
