from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import matplotlib.pyplot as plt
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
        self.principal.sliderAxial.valueChanged.connect(self.actualizar_axial)
        self.principal.sliderCoronal.valueChanged.connect(self.actualizar_coronal)
        self.principal.sliderSagital.valueChanged.connect(self.actualizar_sagital)

        self.principal.btnCargarMat.clicked.connect(self.cargar_mat)
        self.principal.btnMostrarCanales.clicked.connect(self.mostrar_canales)
        self.principal.btnAgregarRuido.clicked.connect(self.agregar_ruido)
        self.principal.btnEstadisticas.clicked.connect(self.mostrar_estadisticas)

        self.principal.btnCargarDatos.clicked.connect(self.cargar_datos)
        self.principal.btnGraficar.clicked.connect(self.graficar_columna)
        self.principal.btnScatter.clicked.connect(self.graficar_scatter)


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
        try:
            resultado = self.modelo_db.validar_usuario(usuario, password)
        except Exception as e:
            self.login.lblMensaje.setText(f"Error de conexión: {e}")
            return

        if resultado:
            self.id_usuario_actual = resultado[0]
            self.principal.txtUsuarioSesion.setText(str(resultado[1]))
            self.principal.txtRolSesion_2.setText(str(resultado[2]))
            self.principal.txtFechaSesion.setText(datetime.now().strftime("%d/%m/%Y %H:%M"))
            self.login.lblMensaje.setText("")
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

        try:
            self.modelo_db.guardar_sesion(self.id_usuario_actual, ruta)
        except Exception as e:
            QMessageBox.warning(self.principal, "DB", str(e))

        imagen_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = imagen_rgb.shape
        qimg = QImage(imagen_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.principal.lblFotoUsuario.setPixmap(QPixmap.fromImage(qimg).scaled(
            self.principal.lblFotoUsuario.width(),
            self.principal.lblFotoUsuario.height(),
            Qt.KeepAspectRatio))

  

    def cargar_dicom(self):
        carpeta = QFileDialog.getExistingDirectory(self.principal, "Seleccionar carpeta DICOM")
        print(f"Carpeta seleccionada: '{carpeta}'")
        if not carpeta:
            return
        try:
            self.modelo_dicom.cargar_dicom(carpeta)
            self.modelo_dicom.extraer_metadata()

            filas = self.modelo_dicom.metadata_para_tabla()
            self.principal.tableMetadatos.setRowCount(len(filas))
            self.principal.tableMetadatos.setColumnCount(2)
            self.principal.tableMetadatos.setHorizontalHeaderLabels(["Campo", "Valor"])
            for i, (clave, valor) in enumerate(filas):
                self.principal.tableMetadatos.setItem(i, 0, QTableWidgetItem(str(clave)))
                self.principal.tableMetadatos.setItem(i, 1, QTableWidgetItem(str(valor)))


            dims = self.modelo_dicom.dimensiones()
            self.principal.sliderAxial.setMinimum(0)
            self.principal.sliderAxial.setMaximum(dims[0] - 1)
            self.principal.sliderCoronal.setMinimum(0)
            self.principal.sliderCoronal.setMaximum(dims[1] - 1)
            self.principal.sliderSagital.setMinimum(0)
            self.principal.sliderSagital.setMaximum(dims[2] - 1)
            
            self.principal.sliderAxial.setValue(dims[0] // 2)
            self.principal.sliderCoronal.setValue(dims[1] // 2)
            self.principal.sliderSagital.setValue(dims[2] // 2)

        except Exception as e:
                print(f"ERROR DICOM: {e}")
                QMessageBox.critical(self.principal, "Error DICOM", str(e))
        

    def actualizar_axial(self, indice):
        if self.modelo_dicom.volumen_3d is None:
            return
        corte = self.modelo_dicom.corte_axial(indice)
        self.corte_actual = self.modelo_dicom.normalizar(corte)
        self.mostrar_imagen(self.corte_actual, self.principal.lblAxial_2)

    def actualizar_coronal(self, indice):
        if self.modelo_dicom.volumen_3d is None:
            return
        corte = self.modelo_dicom.corte_coronal(indice)
        norm = self.modelo_dicom.normalizar(corte)
        norm = np.flipud(norm)
        self.mostrar_imagen(norm, self.principal.lblCoronal_2)

    def actualizar_sagital(self, indice):
        if self.modelo_dicom.volumen_3d is None:
            return
        corte = self.modelo_dicom.corte_sagital(indice)
        norm = self.modelo_dicom.normalizar(corte)
        norm = np.flipud(norm)
        self.mostrar_imagen(norm, self.principal.lblSagital_2)

    def convertir_nifti(self):
        if self.modelo_dicom.volumen_3d is None:
            QMessageBox.warning(self.principal, "NIfTI", "Primero cargue un DICOM")
            return
        ruta, _ = QFileDialog.getSaveFileName(self.principal, "Guardar NIfTI", "", "NIfTI (*.nii)")
        if ruta:
            try:
                self.modelo_dicom.convertir_nifti(ruta)
                QMessageBox.information(self.principal, "NIfTI", f"Guardado en {ruta}")
            except Exception as e:
                QMessageBox.critical(self.principal, "Error", str(e))

    def guardar_csv(self):
        if self.modelo_dicom.volumen_3d is None:
            QMessageBox.warning(self.principal, "CSV", "Primero cargue un DICOM")
            return
        ruta, _ = QFileDialog.getSaveFileName(self.principal, "Guardar CSV", "", "CSV (*.csv)")
        if ruta:
            try:
                self.modelo_dicom.guardar_csv(ruta)
                QMessageBox.information(self.principal, "CSV", f"Guardado en {ruta}")
            except Exception as e:
                QMessageBox.critical(self.principal, "Error", str(e))

    def aplicar_zoom(self):
        if self.corte_actual is None:
            QMessageBox.warning(self.principal, "Zoom", "Primero cargue un DICOM")
            return
        try:
            h, w = self.corte_actual.shape
            x, y = w // 4, h // 4
            ancho, alto = w // 2, h // 2
            
            bgr = cv2.cvtColor(self.corte_actual, cv2.COLOR_GRAY2BGR)
            ancho_mm, alto_mm = self.modelo_dicom.dimensiones_mm(ancho, alto)
            texto = f"{ancho_mm:.1f}x{alto_mm:.1f}mm"
            cv2.rectangle(bgr, (x, y), (x + ancho, y + alto), (0, 255, 255), 2)
            cv2.putText(bgr, texto, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

   
            recorte = self.corte_actual[y:y + alto, x:x + ancho]
            resize = cv2.resize(recorte, (
                self.principal.lblImagenRecortada.width(),
                self.principal.lblImagenRecortada.height()
            ))
            self.recorte_actual = recorte

            # mostrar imagen original con cuadro dibujado
            bgr_rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            h2, w2, ch = bgr_rgb.shape
            qimg = QImage(bgr_rgb.data, w2, h2, ch * w2, QImage.Format_RGB888)
            self.principal.lblImagenOriginal.setPixmap(QPixmap.fromImage(qimg).scaled(
                self.principal.lblImagenOriginal.width(),
                self.principal.lblImagenOriginal.height(),
                Qt.KeepAspectRatio))

  
            self.mostrar_imagen(resize, self.principal.lblImagenRecortada)

        except Exception as e:
            QMessageBox.critical(self.principal, "Error Zoom", str(e))

    def guardar_recorte(self):
        if self.recorte_actual is None:
            QMessageBox.warning(self.principal, "Recorte", "Primero aplique zoom")
            return
        ruta, _ = QFileDialog.getSaveFileName(self.principal, "Guardar recorte", "", "PNG (*.png)")
        if ruta:
            cv2.imwrite(ruta, self.recorte_actual)
            QMessageBox.information(self.principal, "Recorte", f"Guardado en {ruta}")

    def segmentar_imagen(self):
        if self.corte_actual is None:
            QMessageBox.warning(self.principal, "Segmentación", "Primero cargue un DICOM")
            return
        tipo = self.principal.comboSegmentacion.currentText()
        resultado = self.modelo_dicom.segmentar(self.corte_actual, tipo)
        self.mostrar_imagen(resultado, self.principal.lblImagenSegmentada)

    def aplicar_morfologia(self):
        if self.corte_actual is None:
            QMessageBox.warning(self.principal, "Morfología", "Primero cargue un DICOM")
            return
        mapa = {
            "erosión": "erosion",
            "dilatación": "dilatacion",
            "apertura": "apertura",
            "cierre": "cierre",
            "gradiente": "gradiente"
        }
        operacion = mapa.get(self.principal.comboMorfologia.currentText(), "erosion")
        kernel = self.principal.spinKernel.value() or 3
        resultado = self.modelo_dicom.morfologia(self.corte_actual, operacion, kernel)
        self.mostrar_imagen(resultado, self.principal.lblImagenMorfologica)

 

    def cargar_mat(self):
        ruta, _ = QFileDialog.getOpenFileName(self.principal, "Abrir archivo MAT", "", "MAT (*.mat)")
        if not ruta:
            return
        try:
            self.modelo_senales.cargar_mat(ruta, "data")
            dims2d = self.modelo_senales.dimensiones_2d()
            dims3d = self.modelo_senales.dimensiones_3d()
            QMessageBox.information(self.principal, "MAT cargado",
                                    f"3D: {dims3d}\n2D: {dims2d}")
        except Exception as e:
            QMessageBox.critical(self.principal, "Error MAT", str(e))

    def mostrar_canales(self):
        if self.modelo_senales.datos_2d is None:
            QMessageBox.warning(self.principal, "Señales", "Primero cargue un archivo MAT")
            return
        canal_ini = self.principal.spinCanalInicial.value()
        canal_fin = self.principal.spinCanalFinal.value()
        
        if canal_fin < canal_ini:
            QMessageBox.warning(self.principal, "Señales", "Canal final debe ser mayor al inicial")
            return
        
        canales = self.modelo_senales.seleccionar_canales(canal_ini, canal_fin)
        n = canales.shape[0]
        
        if n == 0:
            QMessageBox.warning(self.principal, "Señales", "No hay canales en ese rango")
            return

        fig, axes = plt.subplots(n, 1, figsize=(6, max(3, n * 1.5)))
        if n == 1:
            axes = [axes]
        for i, ax in enumerate(axes):
            ax.plot(canales[i])
            ax.set_ylabel(f"Canal {canal_ini + i}")
        fig.tight_layout()
        self._fig_a_label(fig, self.principal.lblGraficaDesviacion)

    def agregar_ruido(self):
        if self.modelo_senales.datos_2d is None:
            QMessageBox.warning(self.principal, "Señales", "Primero cargue un archivo MAT")
            return
        canal = self.principal.spinCanalInicial.value()
        amplitud = self.principal.spinRuido.value()
        original, modificada = self.modelo_senales.agregar_ruido(canal, amplitud)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4))
        ax1.plot(original, label="Original")
        ax1.set_title(f"Canal {canal} - Original")
        ax2.plot(modificada, color="orange", label="Con ruido")
        ax2.set_title(f"Canal {canal} - Con ruido (amplitud={amplitud})")
        fig.tight_layout()
        self._fig_a_label(fig, self.principal.lblGraficaDesviacion)

    def mostrar_estadisticas(self):
        if self.modelo_senales.datos_3d is None:
            QMessageBox.warning(self.principal, "Señales", "Primero cargue un archivo MAT")
            return

        if self.principal.radioEje0.isChecked():
            eje = 0
        elif self.principal.radioEje1.isChecked():
            eje = 1
        else:
            eje = 2

        promedio, desviacion = self.modelo_senales.estadisticas(eje)

        prom = np.atleast_1d(promedio).flatten()
        desv = np.atleast_1d(desviacion).flatten()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
        ax1.stem(range(len(prom)), prom)
        ax1.set_title(f"Promedio (eje {eje})")
        ax2.stem(range(len(desv)), desv)
        ax2.set_title(f"Desviación estándar (eje {eje})")
        fig.tight_layout()
        self._fig_a_label(fig, self.principal.lblGraficarPromedio)


    def cargar_datos(self):
        ruta, _ = QFileDialog.getOpenFileName(self.principal, "Abrir datos", "",
                                               "CSV/Excel (*.csv *.xlsx *.xls)")
        if not ruta:
            return
        try:
            self.modelo_tabular.cargar(ruta)
            columnas = self.modelo_tabular.get_columnas()

            self.principal.comboColumna1.clear()
            self.principal.comboColumna1.addItems(columnas)
            self.principal.comboColumna1_2.clear()
            self.principal.comboColumna1_2.addItems(columnas)

        
            df = self.modelo_tabular.get_dataframe()
            describe = df.describe().reset_index()
            self.principal.tableDatos.setRowCount(len(describe))
            self.principal.tableDatos.setColumnCount(len(describe.columns))
            self.principal.tableDatos.setHorizontalHeaderLabels(list(describe.columns.astype(str)))
            for i in range(len(describe)):
                for j in range(len(describe.columns)):
                    val = describe.iloc[i, j]
                    texto = f"{val:.4f}" if isinstance(val, float) else str(val)
                    self.principal.tableDatos.setItem(i, j, QTableWidgetItem(texto))

        except Exception as e:
            QMessageBox.critical(self.principal, "Error", str(e))

    def graficar_columna(self):
        if self.modelo_tabular.df is None:
            QMessageBox.warning(self.principal, "Datos", "Primero cargue un archivo")
            return
        columna = self.principal.comboColumna1.currentText()
        datos = self.modelo_tabular.get_columna(columna)

        fig, ax = plt.subplots(figsize=(5, 3))
        datos.plot(ax=ax, title=f"Columna: {columna}")
        ax.set_xlabel("Índice")
        ax.set_ylabel(columna)
        fig.tight_layout()
        self._fig_a_label(fig, self.principal.lblColumnas)

    def graficar_scatter(self):
        if self.modelo_tabular.df is None:
            QMessageBox.warning(self.principal, "Datos", "Primero cargue un archivo")
            return
        col_x = self.principal.comboColumna1_2.currentText()
        col_y = self.principal.comboColumna1.currentText()
        x, y = self.modelo_tabular.get_scatter(col_x, col_y)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.scatter(x, y, alpha=0.6, edgecolors="k", linewidths=0.3)
        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_title(f"Scatter: {col_x} vs {col_y}")
        fig.tight_layout()
        self._fig_a_label(fig, self.principal.lblScatter)


    def mostrar_imagen(self, imagen, label):
        imagen = np.ascontiguousarray(imagen)
        if imagen.ndim == 2:
            h, w = imagen.shape
            qimg = QImage(imagen.data, w, h, w, QImage.Format_Grayscale8)
        else:
            h, w, ch = imagen.shape
            qimg = QImage(imagen.data, w, h, ch * w, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qimg).scaled(
            label.width(), label.height(), Qt.KeepAspectRatio))

    def _fig_a_label(self, fig, label):
        ruta = "temp_fig.png"
        fig.savefig(ruta, dpi=90, bbox_inches="tight")
        plt.close(fig)
        label.setPixmap(QPixmap(ruta).scaled(
            label.width(), label.height(), Qt.KeepAspectRatio))