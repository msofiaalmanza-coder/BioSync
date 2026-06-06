import sys

from PyQt5.QtWidgets import QApplication

from controlador.controlador import Controlador

def main():

    app = QApplication(sys.argv)
    controlador = Controlador()
    controlador.mostrar_main()
    sys.exit(
        app.exec_()
    )

if __name__ == "__main__":

    main()
