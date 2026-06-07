from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFrame, QLabel, QLineEdit,
    QPushButton, QGridLayout, QTabWidget, QTableWidget,
    QComboBox, QSpinBox, QSlider, QRadioButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap


class PrincipalView(QMainWindow):
    sig_tomar_foto            = pyqtSignal()


    sig_cargar_dicom          = pyqtSignal()
    sig_convertir_nifti       = pyqtSignal()
    sig_guardar_csv           = pyqtSignal()
    sig_aplicar_segmentacion  = pyqtSignal()
    sig_generar_zoom          = pyqtSignal()
    sig_guardar_recorte       = pyqtSignal()
    sig_aplicar_morfologia    = pyqtSignal()

    sig_cargar_mat            = pyqtSignal()
    sig_mostrar_canales       = pyqtSignal()
    sig_agregar_ruido         = pyqtSignal()
    sig_calcular_estadisticas = pyqtSignal()

    sig_cargar_datos          = pyqtSignal()
    sig_generar_scatter       = pyqtSignal()
    sig_graficar_columnas     = pyqtSignal()
    sig_salir                 = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_window()
        self._build_ui()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("BioSync - Panel principal")
        self.setMinimumSize(770, 583)
        self.resize(770, 645)

    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        grid = QGridLayout(central)

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        grid.addWidget(self.frame, 0, 0)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setGeometry(20, 10, 760, 583)
        self.tabWidget.setMinimumSize(760, 583)
        self.tabWidget.setStyleSheet("background-color: rgb(230, 230, 230);")

        self._build_tab_inicio()
        self._build_tab_imagenes()
        self._build_tab_senales()
        self._build_tab_tabulares()

    def _build_tab_inicio(self):
        tab = QWidget()
        self.tabWidget.addTab(tab, "Inicio")

        self.lblUsuario = QLabel("Usuario:", tab)
        self.lblUsuario.setGeometry(170, 30, 231, 71)
        self.lblUsuario.setStyleSheet('font: 75 10pt "Times New Roman";')

        self.txtUsuarioSesion = QLineEdit(tab)
        self.txtUsuarioSesion.setGeometry(410, 50, 191, 31)
        self.txtUsuarioSesion.setStyleSheet(
            'background-color: rgb(255, 255, 255); font: 10pt "Times New Roman";'
        )
        self.txtUsuarioSesion.setReadOnly(True)

        self.lblFecha = QLabel("Fecha:", tab)
        self.lblFecha.setGeometry(170, 80, 241, 71)
        self.lblFecha.setStyleSheet('font: 75 10pt "Times New Roman";')

        self.txtFechaSesion = QLineEdit(tab)
        self.txtFechaSesion.setGeometry(410, 100, 191, 31)
        self.txtFechaSesion.setStyleSheet(
            'background-color: rgb(255, 255, 255); font: 10pt "Times New Roman";'
        )
        self.txtFechaSesion.setReadOnly(True)

        self.lblRol = QLabel("Rol:", tab)
        self.lblRol.setGeometry(180, 120, 211, 81)
        self.lblRol.setStyleSheet('font: 75 10pt "Times New Roman";')

        self.txtRolSesion = QLineEdit(tab)
        self.txtRolSesion.setGeometry(410, 150, 191, 31)
        self.txtRolSesion.setStyleSheet(
            'background-color: rgb(255, 255, 255); font: 10pt "Times New Roman";'
        )
        self.txtRolSesion.setReadOnly(True)

        self.lblFotoUsuario = QLabel(tab)
        self.lblFotoUsuario.setGeometry(310, 230, 141, 151)
        self.lblFotoUsuario.setStyleSheet("border-color: rgb(11, 11, 11);")
        self.lblFotoUsuario.setAlignment(Qt.AlignCenter)

        self.btnCapturarFoto = QPushButton("Tomar foto", tab)
        self.btnCapturarFoto.setGeometry(280, 400, 201, 81)
        self.btnCapturarFoto.setStyleSheet(
            'font: 75 12pt "Times New Roman"; background-color: rgb(194, 225, 252);'
        )

    def _build_tab_imagenes(self):
        tab = QWidget()
        self.tabWidget.addTab(tab, "Imágenes médicas")

        BTN_STYLE = 'font: 75 8pt "Times New Roman"; background-color: rgb(194, 225, 252);'

        self.btnCargarDicom = QPushButton("Cargar DICOM", tab)
        self.btnCargarDicom.setGeometry(10, 20, 131, 31)
        self.btnCargarDicom.setStyleSheet(BTN_STYLE)

        self.btnConvertirNifti = QPushButton("Convertir a NIFTI", tab)
        self.btnConvertirNifti.setGeometry(10, 60, 131, 31)
        self.btnConvertirNifti.setStyleSheet(BTN_STYLE)

        self.btnGuardarCSV = QPushButton("Guardar CSV", tab)
        self.btnGuardarCSV.setGeometry(10, 100, 131, 31)
        self.btnGuardarCSV.setStyleSheet(BTN_STYLE)

        self.tableMetadatos = QTableWidget(tab)
        self.tableMetadatos.setGeometry(170, 10, 491, 191)
        self.tableMetadatos.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.label_tipo_seg = QLabel(tab)
        self.label_tipo_seg.setGeometry(10, 140, 141, 41)
        self.label_tipo_seg.setStyleSheet('font: 75 11pt "Times New Roman";')
        self.label_tipo_seg.setText(
            '<html><body><p align="center">'
            '<span style=" font-size:8pt;">Tipo segmentación</span>'
            '</p></body></html>'
        )

        self.comboSegmentacion = QComboBox(tab)
        self.comboSegmentacion.setGeometry(20, 190, 101, 41)
        self.comboSegmentacion.setStyleSheet("background-color: rgb(255, 255, 255);")
        for op in ["binary", "binary_inv", "trunc", "tozero", "tozero_inv"]:
            self.comboSegmentacion.addItem(op)

        self.btnSegmentar = QPushButton("Aplicar segmentación", tab)
        self.btnSegmentar.setGeometry(10, 240, 161, 41)
        self.btnSegmentar.setStyleSheet(BTN_STYLE)

        self.frame_vistas = QFrame(tab)
        self.frame_vistas.setGeometry(270, 210, 311, 181)
        self.frame_vistas.setFrameShape(QFrame.StyledPanel)
        self.frame_vistas.setFrameShadow(QFrame.Raised)

        for nombre, lbl_geo, img_geo, slider_geo in [
            ("Axial",   (20,  10, 51, 31), (10,  60, 81, 71), (10,  150, 91, 16)),
            ("Coronal", (120, 10, 61, 31), (110, 60, 81, 71), (110, 150, 91, 16)),
            ("Sagital", (240, 10, 51, 31), (210, 60, 81, 71), (210, 150, 91, 16)),
        ]:
            key = nombre.lower()

            lbl_titulo = QLabel(self.frame_vistas)
            lbl_titulo.setGeometry(*lbl_geo)
            lbl_titulo.setStyleSheet(
                'font: 75 8pt "Times New Roman"; background-color: rgb(255, 255, 255);'
            )
            lbl_titulo.setFrameShape(QFrame.Box)
            lbl_titulo.setAlignment(Qt.AlignCenter)
            lbl_titulo.setText(nombre)
            setattr(self, f"lbl{nombre}Titulo", lbl_titulo)

            lbl_img = QLabel(self.frame_vistas)
            lbl_img.setGeometry(*img_geo)
            lbl_img.setStyleSheet("border-color: rgb(12, 12, 12);")
            setattr(self, f"lbl{nombre}", lbl_img)

            slider = QSlider(Qt.Horizontal, self.frame_vistas)
            slider.setGeometry(*slider_geo)
            setattr(self, f"slider{nombre}", slider)

        self.lblImagenOriginal = QLabel(tab)
        self.lblImagenOriginal.setGeometry(20, 320, 81, 111)

        self.lblImagenRecortada = QLabel(tab)
        self.lblImagenRecortada.setGeometry(130, 319, 81, 111)

        self.btnZoom = QPushButton("Generar Zoom", tab)
        self.btnZoom.setGeometry(10, 450, 111, 51)
        self.btnZoom.setStyleSheet(BTN_STYLE)

        self.btnGuardarRecorte = QPushButton("Guardar recorte", tab)
        self.btnGuardarRecorte.setGeometry(130, 450, 121, 51)
        self.btnGuardarRecorte.setStyleSheet(BTN_STYLE)

        self.label_transf_morf = QLabel(tab)
        self.label_transf_morf.setGeometry(420, 400, 221, 41)
        self.label_transf_morf.setStyleSheet('font: 75 11pt "Times New Roman";')
        self.label_transf_morf.setText(
            '<html><body><p align="center">'
            '<span style=" font-size:8pt;">Transformación morfológica</span>'
            '</p></body></html>'
        )

        self.label_kernel = QLabel(tab)
        self.label_kernel.setGeometry(430, 450, 91, 21)
        self.label_kernel.setStyleSheet('font: 75 8pt "Times New Roman";')
        self.label_kernel.setText(
            '<html><body><p align="center">Kernel</p></body></html>'
        )

        self.comboMorfologia = QComboBox(tab)
        self.comboMorfologia.setGeometry(530, 451, 111, 41)
        self.comboMorfologia.setStyleSheet("background-color: rgb(255, 255, 255);")
        for op in ["erosión", "dilatación", "apertura", "cierre", "gradiente"]:
            self.comboMorfologia.addItem(op)

        self.spinKernel = QSpinBox(tab)
        self.spinKernel.setGeometry(460, 470, 42, 22)

        self.btnMorfologia = QPushButton("Aplicar morfología", tab)
        self.btnMorfologia.setGeometry(440, 510, 181, 31)
        self.btnMorfologia.setStyleSheet(BTN_STYLE)

    def _build_tab_senales(self):
        tab = QWidget()
        self.tabWidget.addTab(tab, "Señales biomédicas")

        BTN_STYLE_LG = 'font: 75 10pt "Times New Roman"; background-color: rgb(194, 225, 252);'
        BTN_STYLE_SM = 'font: 75 8pt "Times New Roman"; background-color: rgb(194, 225, 252);'

        self.btnCargarMat = QPushButton("Cargar MAT", tab)
        self.btnCargarMat.setGeometry(30, 90, 131, 101)
        self.btnCargarMat.setStyleSheet(BTN_STYLE_LG)

        self.label_canal_ini = QLabel(tab)
        self.label_canal_ini.setGeometry(220, 20, 111, 51)
        self.label_canal_ini.setStyleSheet('font: 11pt "Times New Roman";')
        self.label_canal_ini.setText(
            '<html><body><p align="center">Canal inicial</p></body></html>'
        )

        self.spinCanalInicial = QSpinBox(tab)
        self.spinCanalInicial.setGeometry(260, 70, 42, 22)
        self.spinCanalInicial.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.label_canal_fin = QLabel(tab)
        self.label_canal_fin.setGeometry(340, 20, 91, 51)
        self.label_canal_fin.setStyleSheet('font: 75 11pt "Times New Roman";')
        self.label_canal_fin.setText(
            '<html><body><p align="center">Canal final</p></body></html>'
        )

        self.spinCanalFinal = QSpinBox(tab)
        self.spinCanalFinal.setGeometry(370, 70, 42, 22)
        self.spinCanalFinal.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.btnMostrarCanales = QPushButton("Mostrar Canales", tab)
        self.btnMostrarCanales.setGeometry(220, 110, 121, 61)
        self.btnMostrarCanales.setStyleSheet(BTN_STYLE_SM)

        self.btnAgregarRuido = QPushButton("Agregar Ruido", tab)
        self.btnAgregarRuido.setGeometry(360, 110, 131, 61)
        self.btnAgregarRuido.setStyleSheet(BTN_STYLE_SM)

        self.label_eje = QLabel(tab)
        self.label_eje.setGeometry(490, 50, 181, 16)
        self.label_eje.setStyleSheet('font: 75 8pt "Times New Roman";')
        self.label_eje.setText(
            '<html><body><p align="center">Eje de análisis</p></body></html>'
        )

        self.radioEje0 = QRadioButton("x", tab)
        self.radioEje0.setGeometry(560, 70, 62, 21)
        self.radioEje0.setStyleSheet('font: 75 11pt "Times New Roman";')

        self.radioEje1 = QRadioButton("y", tab)
        self.radioEje1.setGeometry(560, 110, 62, 21)
        self.radioEje1.setStyleSheet('font: 75 11pt "Times New Roman";')

        self.radioEje2 = QRadioButton("z", tab)
        self.radioEje2.setGeometry(560, 150, 62, 21)
        self.radioEje2.setStyleSheet('font: 75 11pt "Times New Roman";')

        self.lblGraficaDesviacion = QLabel(tab)
        self.lblGraficaDesviacion.setGeometry(120, 240, 211, 141)
        self.lblGraficaDesviacion.setAlignment(Qt.AlignCenter)

        self.lblGraficarPromedio = QLabel(tab)
        self.lblGraficarPromedio.setGeometry(440, 240, 211, 141)
        self.lblGraficarPromedio.setAlignment(Qt.AlignCenter)

        self.btnEstadisticas = QPushButton("Calcular Estadísticas", tab)
        self.btnEstadisticas.setGeometry(310, 410, 141, 71)
        self.btnEstadisticas.setStyleSheet(BTN_STYLE_SM)

    def _build_tab_tabulares(self):
        tab = QWidget()
        self.tabWidget.addTab(tab, "Datos tabulares")

        BTN_STYLE_LG = 'font: 75 10pt "Times New Roman"; background-color: rgb(194, 225, 252);'
        BTN_STYLE_SM = 'font: 75 8pt "Times New Roman"; background-color: rgb(194, 225, 252);'

        self.btnCargarDatos = QPushButton("Cargar archivos", tab)
        self.btnCargarDatos.setGeometry(30, 50, 131, 51)
        self.btnCargarDatos.setStyleSheet(BTN_STYLE_LG)

        self.comboColumna1 = QComboBox(tab)
        self.comboColumna1.setGeometry(220, 50, 191, 41)
        self.comboColumna1.setStyleSheet(
            'font: 75 10pt "Times New Roman"; background-color: rgb(255, 255, 255);'
        )

        self.comboColumna2 = QComboBox(tab)
        self.comboColumna2.setGeometry(450, 50, 191, 41)
        self.comboColumna2.setStyleSheet(
            'font: 75 10pt "Times New Roman"; background-color: rgb(255, 255, 255);'
        )

        self.tableDatos = QTableWidget(tab)
        self.tableDatos.setGeometry(20, 150, 401, 291)

        self.btnScatter = QPushButton("Generar Scatter", tab)
        self.btnScatter.setGeometry(470, 200, 131, 61)
        self.btnScatter.setStyleSheet(BTN_STYLE_SM)

        self.btnGraficar = QPushButton("Graficar columnas", tab)
        self.btnGraficar.setGeometry(470, 290, 131, 61)
        self.btnGraficar.setStyleSheet(BTN_STYLE_SM)

        self.btnSalirApp = QPushButton("SALIR", tab)
        self.btnSalirApp.setGeometry(540, 500, 131, 41)
        self.btnSalirApp.setStyleSheet(
            'font: 75 10pt "Times New Roman"; background-color: rgb(255, 255, 255);'
        )


    def _connect_signals(self):
  
        self.btnCapturarFoto.clicked.connect(self.sig_tomar_foto)


        self.btnCargarDicom.clicked.connect(self.sig_cargar_dicom)
        self.btnConvertirNifti.clicked.connect(self.sig_convertir_nifti)
        self.btnGuardarCSV.clicked.connect(self.sig_guardar_csv)
        self.btnSegmentar.clicked.connect(self.sig_aplicar_segmentacion)
        self.btnZoom.clicked.connect(self.sig_generar_zoom)
        self.btnGuardarRecorte.clicked.connect(self.sig_guardar_recorte)
        self.btnMorfologia.clicked.connect(self.sig_aplicar_morfologia)

        self.btnCargarMat.clicked.connect(self.sig_cargar_mat)
        self.btnMostrarCanales.clicked.connect(self.sig_mostrar_canales)
        self.btnAgregarRuido.clicked.connect(self.sig_agregar_ruido)
        self.btnEstadisticas.clicked.connect(self.sig_calcular_estadisticas)

        self.btnCargarDatos.clicked.connect(self.sig_cargar_datos)
        self.btnScatter.clicked.connect(self.sig_generar_scatter)
        self.btnGraficar.clicked.connect(self.sig_graficar_columnas)
        self.btnSalirApp.clicked.connect(self.sig_salir)

    def set_datos_sesion(self, usuario: str, fecha: str, rol: str):
        self.txtUsuarioSesion.setText(usuario)
        self.txtFechaSesion.setText(fecha)
        self.txtRolSesion.setText(rol)

    def set_foto_usuario(self, pixmap: QPixmap):
        self.lblFotoUsuario.setPixmap(
            pixmap.scaled(self.lblFotoUsuario.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


    def set_imagen_axial(self, pixmap: QPixmap):
        self.lblAxial.setPixmap(
            pixmap.scaled(self.lblAxial.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def set_imagen_coronal(self, pixmap: QPixmap):
        self.lblCoronal.setPixmap(
            pixmap.scaled(self.lblCoronal.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def set_imagen_sagital(self, pixmap: QPixmap):
        self.lblSagital.setPixmap(
            pixmap.scaled(self.lblSagital.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def set_imagen_original(self, pixmap: QPixmap):
        self.lblImagenOriginal.setPixmap(
            pixmap.scaled(self.lblImagenOriginal.size(), Qt.KeepAspectRatio)
        )

    def set_imagen_recortada(self, pixmap: QPixmap):
        self.lblImagenRecortada.setPixmap(
            pixmap.scaled(self.lblImagenRecortada.size(), Qt.KeepAspectRatio)
        )

    def set_metadatos(self, headers: list, filas: list):
        from PyQt5.QtWidgets import QTableWidgetItem
        self.tableMetadatos.setColumnCount(len(headers))
        self.tableMetadatos.setHorizontalHeaderLabels(headers)
        self.tableMetadatos.setRowCount(len(filas))
        for r, fila in enumerate(filas):
            for c, valor in enumerate(fila):
                self.tableMetadatos.setItem(r, c, QTableWidgetItem(str(valor)))

    def get_tipo_segmentacion(self) -> str:
        return self.comboSegmentacion.currentText()

    def get_tipo_morfologia(self) -> str:
        return self.comboMorfologia.currentText()

    def get_kernel(self) -> int:
        return self.spinKernel.value()

    def get_slice_axial(self) -> int:
        return self.sliderAxial.value()

    def get_slice_coronal(self) -> int:
        return self.sliderCoronal.value()

    def get_slice_sagital(self) -> int:
        return self.sliderSagital.value()


    def get_canal_inicial(self) -> int:
        return self.spinCanalInicial.value()

    def get_canal_final(self) -> int:
        return self.spinCanalFinal.value()

    def get_eje_analisis(self) -> int:
   
        if self.radioEje0.isChecked():
            return 0
        if self.radioEje1.isChecked():
            return 1
        return 2

    def set_grafica_promedio(self, pixmap: QPixmap):
        self.lblGraficarPromedio.setPixmap(
            pixmap.scaled(self.lblGraficarPromedio.size(), Qt.KeepAspectRatio)
        )

    def set_grafica_desviacion(self, pixmap: QPixmap):
        self.lblGraficaDesviacion.setPixmap(
            pixmap.scaled(self.lblGraficaDesviacion.size(), Qt.KeepAspectRatio)
        )


    def poblar_combos_columnas(self, columnas: list):
   
        for combo in [self.comboColumna1, self.comboColumna2]:
            combo.clear()
            for col in columnas:
                combo.addItem(col)

    def get_columna1(self) -> str:
        return self.comboColumna1.currentText()

    def get_columna2(self) -> str:
        return self.comboColumna2.currentText()

    def set_tabla_datos(self, headers: list, filas: list):
        """Popula la tabla de datos tabulares."""
        from PyQt5.QtWidgets import QTableWidgetItem
        self.tableDatos.setColumnCount(len(headers))
        self.tableDatos.setHorizontalHeaderLabels(headers)
        self.tableDatos.setRowCount(len(filas))
        for r, fila in enumerate(filas):
            for c, valor in enumerate(fila):
                self.tableDatos.setItem(r, c, QTableWidgetItem(str(valor)))
