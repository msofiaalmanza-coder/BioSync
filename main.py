import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic

app = QApplication(sys.argv)

try:
    ventana = uic.loadUi("Vista/main.ui")
    ventana.show()
    app.exec_()
except Exception as e:
    print("Error:", e)
