from Vista.vista_bienvenida import VistaBienvenida
from Vista.vista_login import VistaLogin
from Vista.vista_principal import VistaPrincipal


class Controlador:

    def __init__(self):

        self.vista_bienvenida = VistaBienvenida()
        self.vista_login = VistaLogin()
        self.vista_principal = VistaPrincipal()

        self.conectar_eventos()

    def conectar_eventos(self):

        # =========================
        # BIENVENIDA
        # =========================

        self.vista_bienvenida.btnIngresar.clicked.connect(
            self.abrir_login
        )

        self.vista_bienvenida.btnSalir.clicked.connect(
            self.salir
        )

        # =========================
        # LOGIN
        # =========================

        self.vista_login.btnLogin.clicked.connect(
            self.iniciar_sesion
        )

        self.vista_login.btnVolver.clicked.connect(
            self.volver_bienvenida
        )

        # =========================
        # IMÁGENES MÉDICAS
        # =========================

        self.vista_principal.btnCargarDicom.clicked.connect(
            self.cargar_dicom
        )

        self.vista_principal.btnConvertirNifti.clicked.connect(
            self.convertir_nifti
        )

        self.vista_principal.btnGuardarCSV.clicked.connect(
            self.guardar_csv
        )

        self.vista_principal.btnGuardarExcel.clicked.connect(
            self.guardar_excel
        )

        self.vista_principal.btnZoom.clicked.connect(
            self.aplicar_zoom
        )

        self.vista_principal.btnGuardarRecorte.clicked.connect(
            self.guardar_recorte
        )

        self.vista_principal.btnSegmentar.clicked.connect(
            self.segmentar
        )

        self.vista_principal.btnMorfologia.clicked.connect(
            self.morfologia
        )

        # =========================
        # SEÑALES BIOMÉDICAS
        # =========================

        self.vista_principal.btnCargarMat.clicked.connect(
            self.cargar_mat
        )

        self.vista_principal.btnMostrarCanales.clicked.connect(
            self.mostrar_canales
        )

        self.vista_principal.btnAgregarRuido.clicked.connect(
            self.agregar_ruido
        )

        self.vista_principal.btnEstadisticas.clicked.connect(
            self.calcular_estadisticas
        )

        # =========================
        # DATOS TABULARES
        # =========================

        self.vista_principal.btnCargarDatos.clicked.connect(
            self.cargar_datos
        )

        self.vista_principal.btnGraficar.clicked.connect(
            self.graficar_columnas
        )

        self.vista_principal.btnScatter.clicked.connect(
            self.graficar_scatter
        )

    # ==================================
    # NAVEGACIÓN
    # ==================================

    def iniciar(self):
        self.vista_bienvenida.show()

    def abrir_login(self):

        self.vista_bienvenida.hide()
        self.vista_login.show()

    def volver_bienvenida(self):

        self.vista_login.hide()
        self.vista_bienvenida.show()

    def iniciar_sesion(self):

        usuario = self.vista_login.txtUsuario.text()
        password = self.vista_login.txtPassword.text()

        if usuario != "" and password != "":

            self.vista_login.hide()

            self.vista_principal.txtUsuarioSesion.setText(usuario)

            self.vista_principal.show()

    def salir(self):

        self.vista_bienvenida.close()

    # ==================================
    # IMÁGENES MÉDICAS
    # ==================================

    def cargar_dicom(self):
        print("Cargar DICOM")

    def convertir_nifti(self):
        print("Convertir NIFTI")

    def guardar_csv(self):
        print("Guardar CSV")

    def guardar_excel(self):
        print("Guardar Excel")

    def aplicar_zoom(self):
        print("Zoom")

    def guardar_recorte(self):
        print("Guardar recorte")

    def segmentar(self):
        print("Segmentar")

    def morfologia(self):
        print("Morfología")

    # ==================================
    # SEÑALES BIOMÉDICAS
    # ==================================

    def cargar_mat(self):
        print("Cargar MAT")

    def mostrar_canales(self):
        print("Mostrar canales")

    def agregar_ruido(self):
        print("Agregar ruido")

    def calcular_estadisticas(self):
        print("Calcular estadísticas")

    # ==================================
    # DATOS TABULARES
    # ==================================

    def cargar_datos(self):
        print("Cargar datos")

    def graficar_columnas(self):
        print("Graficar columnas")

    def graficar_scatter(self):
        print("Scatter")