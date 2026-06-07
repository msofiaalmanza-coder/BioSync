
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFrame, QLabel, QLineEdit,
    QPushButton, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal


class LoginView(QMainWindow):

    sig_login    = pyqtSignal()
    sig_cancelar = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window()
        self._build_ui()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("Login - BioSync")
        self.setMinimumSize(770, 583)
        self.resize(782, 631)

    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)

        grid = QGridLayout(central)

      
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        grid.addWidget(self.frame, 0, 0)

        self.lblTitulo = QLabel(self.frame)
        self.lblTitulo.setGeometry(290, 20, 151, 61)
        self.lblTitulo.setStyleSheet('font: 75 20pt "Times New Roman";')
        self.lblTitulo.setAlignment(Qt.AlignCenter)
        self.lblTitulo.setText(
            '<html><body><p align="center">'
            '<span style=" font-size:22pt;">LOGIN</span>'
            '</p></body></html>'
        )

        self.lblusuario = QLabel(self.frame)
        self.lblusuario.setGeometry(140, 30, 431, 151)
        self.lblusuario.setStyleSheet('font: 75 12pt "Times New Roman";')
        self.lblusuario.setText(
            '<html><body><p align="justify">Ingresa el nombre del usuario: </p></body></html>'
        )

    
        self.txtUsuario = QLineEdit(self.frame)
        self.txtUsuario.setGeometry(430, 90, 171, 31)
        self.txtUsuario.setStyleSheet(
            'background-color: rgb(255, 255, 255);'
            'font: 10pt "Times New Roman";'
        )
        self.txtUsuario.setPlaceholderText("Usuario")

        self.label = QLabel(self.frame)
        self.label.setGeometry(220, 140, 521, 141)
        self.label.setStyleSheet('font: 75 12pt "Times New Roman";')
        self.label.setText("Ingresa la contraseña:")


        self.txtPassword = QLineEdit(self.frame)
        self.txtPassword.setGeometry(430, 190, 171, 41)
        self.txtPassword.setStyleSheet(
            'background-color: rgb(255, 255, 255);'
            'font: 10pt "Times New Roman";'
        )
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setPlaceholderText("Contraseña")

        self.btnLogin = QPushButton("Ingresar", self.frame)
        self.btnLogin.setGeometry(300, 290, 151, 51)
        self.btnLogin.setStyleSheet(
            'font: 75 12pt "Times New Roman";'
            'background-color: rgb(194, 225, 252);'
        )

        self.lblMensaje = QLabel(self.frame)
        self.lblMensaje.setGeometry(200, 350, 361, 31)
        self.lblMensaje.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.lblMensaje.setAlignment(Qt.AlignCenter)
        self.lblMensaje.setText("")

        self.btnVolver = QPushButton("Cancelar", self.frame)
        self.btnVolver.setGeometry(300, 390, 151, 51)
        self.btnVolver.setStyleSheet(
            'font: 75 12pt "Times New Roman";'
            'background-color: rgb(194, 225, 252);'
        )

    def _connect_signals(self):
        self.btnLogin.clicked.connect(self.sig_login)
        self.btnVolver.clicked.connect(self.sig_cancelar)

 

    def get_usuario(self) -> str:
        """Retorna el texto escrito en el campo de usuario."""
        return self.txtUsuario.text().strip()

    def get_password(self) -> str:
        """Retorna el texto escrito en el campo de contraseña."""
        return self.txtPassword.text()

    def set_mensaje(self, texto: str, color: str = "red"):
        """
        Muestra un mensaje de retroalimentación (error o éxito).

        Args:
            texto:  Texto a mostrar.
            color:  Color CSS del texto (por defecto rojo para errores).
        """
        self.lblMensaje.setStyleSheet(
            f"background-color: rgb(230, 230, 230); color: {color};"
        )
        self.lblMensaje.setText(texto)

    def limpiar_campos(self):
        """Borra los campos de usuario y contraseña."""
        self.txtUsuario.clear()
        self.txtPassword.clear()
        self.lblMensaje.setText("")

    def limpiar_mensaje(self):
        """Borra solo el mensaje de retroalimentación."""
        self.lblMensaje.setText("")
