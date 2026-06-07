from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import os
from datetime import datetime

from modelo.modelo_db import ModeloDB
from modelo.modelo_dicom import DicomModel
from modelo.modelo_señales import SenalesModel
from modelo.modelo_tabular import ModeloTabular


class Controlador:

    def __init__(self):
        self.main = uic.loadUi("vista/main.ui")
        self.login = uic.loadUi("vista/login.ui")
        self.principal = uic.loadUi("vista/principal.ui")

        self.modelo_db = ModeloDB()
        self.modelo_dicom = DicomModel()
        self.modelo_senales = SenalesModel()
        self.modelo_tabular = ModeloTabular()

        self.id_usuario_actual = None
        self.corte_actual = None
        self.recorte_actual = None

        self.conectar_eventos()

    def conectar_eventos(self):
        self.main.btnIngresar.clicked.connect(self.abrir_login)
        self.main.btnSalir.clicked.connect(self.cerrar_app)

        self.login.btnLogin.clicked.connect(self.validar_login)
        self.login.btnVolver.clicked.connect(self.volver_main)

        self.principal.btnCapturarFoto.clicked.connect(self.capturar_foto)
        self.principal.pushButton.clicked.connect(self.cerrar_app)

        self.principal.btnCargarDicom.clicked.connect(self.cargar_dicom)
        self.principal.btnConvertirNifti.clicked.connect(self.convertir_nifti)
        self.principal.btnGuardarCSV.clicked.connect(self.guardar_csv)
        self.principal.btnZoom.clicked.connect(self.aplicar_zoom)
        self.principal.btnGuardarRecorte.clicked.connect(self.guardar_recorte)
        self.principal.btnSegmentar.clicked.connect(self.segmentar_imagen)
        self.principal.btnMorfologia.clicked.connect(self.aplicar_morfologia)

        self.principal.btnCargarMat.clicked.connect(self.cargar_mat)
        self.principal.btnAgregarRuido.clicked.connect(self.agregar_ruido)
        self.principal.btnMostrarCanales.clicked.connect(self.mostrar_canales)
        self.principal.btnEstadisticas.clicked.connect(self.mostrar_estadisticas)

        self.principal.btnCargarDatos.clicked.connect(self.cargar_datos)
        self.principal.btnGraficar.clicked.connect(self.graficar_columna)
        self.principal.btnScatter.clicked.connect(self.graficar_scatter)

    # navegacion
    def mostrar_main(self):
        self.main.show()

    def abrir_login(self):
        self.main.hide()
        self.login.show()

    def volver_main(self):
        self.login.hide()
        self.main.show()

    def cerrar_app(self):
        try:
            self.modelo_db.cerrar()
        except:
            pass
        self.main.close()
        self.login.close()
        self.principal.close()

 
    def validar_login(self):
        usuario = self.login.txtUsuario.text()
        password = self.login.txtPassword.text()

        resultado = self.modelo_db.validar_usuario(usuario, password)

        if resultado:
            self.id_usuario_actual = resultado[0]
            self.principal.txtUsuarioSesion.setText(str(resultado[1]))
            self.principal.txtRolSesion_2.setText(str(resultado[2]))
            self.principal.txtFechaSesion.setText(datetime.now().strftime("%d/%m/%Y %H:%M"))
            self.login.hide()
            self.principal.show()
        else:
            self.login.lblMensaje.setText("Usuario o contraseña incorrectos")

  
    def capturar_foto(self):
        camara = cv2.VideoCapture(0)
        ret, frame = camara.read()
        camara.release()

        if not ret:
            QMessageBox.warning(self.principal, "Error", "No se pudo capturar la foto")
            return

        os.makedirs("fotos", exist_ok=True)
        nombre = f"foto_{self.id_usuario_actual}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        ruta = os.path.join("fotos", nombre)
        cv2.imwrite(ruta, frame)

        self.modelo_db.guardar_sesion(self.id_usuario_actual, ruta)

        imagen_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = imagen_rgb.shape
        qimg = QImage(imagen_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.principal.lblFoto.setPixmap(QPixmap.fromImage(qimg).scaled(
            self.principal.lblFoto.width(), self.principal.lblFoto.height(), Qt.KeepAspectRatio))

    # dicom
    def cargar_dicom(self):
        carpeta = QFileDialog.getExistingDirectory(self.principal, "Seleccionar carpeta DICOM")
        if not carpeta:
            return
        try:
            self.modelo_dicom.cargar_dicom(carpeta)
            meta = self.modelo_dicom.extraer_metadata()

            filas = self.modelo_dicom.metadata_para_tabla()
            self.principal.tablaMetadata.setRowCount(len(filas))
            for i, (clave, valor) in enumerate(filas):
                self.principal.tablaMetadata.setItem(i, 0, QTableWidgetItem(str(clave)))
                self.principal.tablaMetadata.setItem(i, 1, QTableWidgetItem(str(valor)))

            indice = self.modelo_dicom.dimensiones()[0] // 2
            corte = self.modelo_dicom.corte_axial(indice)
            self.corte_actual = self.modelo_dicom.normalizar(corte)
            self.mostrar_imagen(self.corte_actual, self.principal.lblDicom)

        except Exception as e:
            QMessageBox.critical(self.principal, "Error DICOM", str(e))

    def convertir_nifti(self):
        ruta, _ = QFileDialog.getSaveFileName(self.principal, "Guardar NIfTI", "", "NIfTI (*.nii)")
        if ruta:
            self.modelo_dicom.convertir_nifti(ruta)
            QMessageBox.information(self.principal, "NIfTI", f"Guardado en {ruta}")

    def guardar_csv(self):
        ruta, _ = QFileDialog.getSaveFileName(self.principal, "Guardar CSV", "", "CSV (*.csv)")
        if ruta:
            self.modelo_dicom.guardar_csv(ruta)
            QMessageBox.information(self.principal, "CSV", f"Guardado en {ruta}")

    def aplicar_zoom(self):
        if self.corte_actual is None:
            return
        x = self.principal.spinX.value()
        y = self.principal.spinY.value()
        ancho = self.principal.spinAncho.value()
        alto = self.principal.spinAlto.value()
        recorte, resize = self.modelo_dicom.zoom(self.corte_actual, x, y, ancho, alto)
        self.recorte_actual = recorte
        self.mostrar_imagen(resize, self.principal.lblZoom)

    def guardar_recorte(self):
        if self.recorte_actual is None:
            return
        ruta, _ = QFileDialog.getSaveFileName(self.principal, "Guardar recorte", "", "PNG (*.png)")
        if ruta:
            cv2.imwrite(ruta, self.recorte_actual)
            QMessageBox.information(self.principal, "Recorte", f"Guardado en {ruta}")

    def segmentar_imagen(self):
        if self.corte_actual is None:
            return
        tipo = self.principal.comboTipoSegmentacion.currentText()
        threshold = self.principal.spinThreshold.value()
        resultado = self.modelo_dicom.segmentar(self.corte_actual, tipo, threshold)
        self.mostrar_imagen(resultado, self.principal.lblSegmentacion)

    def aplicar_morfologia(self):
        if self.corte_actual is None:
            return
        operacion = self.principal.comboMorfologia.currentText()
        kernel = self.principal.spinKernel.value()
        resultado = self.modelo_dicom.morfologia(self.corte_actual, operacion, kernel)
        self.mostrar_imagen(resultado, self.principal.lblMorfologia)

   
    def cargar_mat(self):
        ruta, _ = QFileDialog.getOpenFileName(self.principal, "Abrir archivo MAT", "", "MAT (*.mat)")
        if not ruta:
            return
        variable = self.principal.txtVariableMat.text()
        try:
            self.modelo_senales.cargar_mat(ruta, variable)
            dims = self.modelo_senales.dimensiones_2d()
            self.principal.lblInfoMat.setText(f"Dimensiones 2D: {dims}")
        except Exception as e:
            QMessageBox.critical(self.principal, "Error MAT", str(e))

    def agregar_ruido(self):
        canal = self.principal.spinCanal.value()
        amplitud = self.principal.spinAmplitud.value()
        original, modificada = self.modelo_senales.agregar_ruido(canal, amplitud)

        fig = self.principal.canvasRuido.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(original, label="Original")
        ax.plot(modificada, label="Con ruido")
        ax.legend()
        self.principal.canvasRuido.draw()

    def mostrar_canales(self):
        canal_ini = self.principal.spinCanalIni.value()
        canal_fin = self.principal.spinCanalFin.value()
        canales = self.modelo_senales.seleccionar_canales(canal_ini, canal_fin)

        fig = self.principal.canvasCanales.figure
        fig.clear()
        for i in range(canales.shape[0]):
            ax = fig.add_subplot(canales.shape[0], 1, i + 1)
            ax.plot(canales[i])
            ax.set_ylabel(f"Canal {canal_ini + i}")
        fig.tight_layout()
        self.principal.canvasCanales.draw()

    def mostrar_estadisticas(self):
        eje = self.principal.spinEje.value()
        promedio, desviacion = self.modelo_senales.estadisticas(eje)
        QMessageBox.information(
            self.principal, "Estadísticas",
            f"Promedio: {np.round(promedio, 4)}\nDesviación: {np.round(desviacion, 4)}"
        )

    # tabular
    def cargar_datos(self):
        ruta, _ = QFileDialog.getOpenFileName(self.principal, "Abrir datos", "", "CSV/Excel (*.csv *.xlsx)")
        if not ruta:
            return
        try:
            self.modelo_tabular.cargar(ruta)
            columnas = self.modelo_tabular.get_columnas()
            self.principal.comboColumna.addItems(columnas)
            self.principal.comboX.addItems(columnas)
            self.principal.comboY.addItems(columnas)
        except Exception as e:
            QMessageBox.critical(self.principal, "Error", str(e))

    def graficar_columna(self):
        columna = self.principal.comboColumna.currentText()
        datos = self.modelo_tabular.get_columna(columna)

        fig = self.principal.canvasTabular.figure
        fig.clear()
        ax = fig.add_subplot(111)
        datos.plot(ax=ax, title=columna)
        self.principal.canvasTabular.draw()

    def graficar_scatter(self):
        col_x = self.principal.comboX.currentText()
        col_y = self.principal.comboY.currentText()
        x, y = self.modelo_tabular.get_scatter(col_x, col_y)

        fig = self.principal.canvasTabular.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.scatter(x, y)
        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        self.principal.canvasTabular.draw()

    def mostrar_imagen(self, imagen, label):
        h, w = imagen.shape
        qimg = QImage(imagen.data, w, h, w, QImage.Format_Grayscale8)
        label.setPixmap(QPixmap.fromImage(qimg).scaled(
            label.width(), label.height(), Qt.KeepAspectRatio))