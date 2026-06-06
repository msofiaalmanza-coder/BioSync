import numpy as np
from scipy.io import loadmat


class SenalesModel:

    def __init__(self):
        self.datos_3d = None
        self.datos_2d = None

    def cargar_mat(self, ruta, variable):
        archivo = loadmat(ruta)

        if variable not in archivo:
            raise ValueError("Variable no encontrada.")

        self.datos_3d = np.array(archivo[variable])
        self.reshape_2d()

        return self.datos_3d

    def reshape_2d(self):
        if self.datos_3d is None:
            raise ValueError("No hay datos cargados.")

        dimensiones = self.datos_3d.shape

        self.datos_2d = self.datos_3d.reshape(
            dimensiones[0],
            -1
        )

        return self.datos_2d

    def seleccionar_canales(self, canal_inicial, canal_final):
        return self.datos_2d[
            canal_inicial:canal_final + 1,
            :
        ]

    def obtener_canal(self, canal):
        return self.datos_2d[canal, :]

    def agregar_ruido(self, canal, amplitud=0.1):
        original = self.obtener_canal(canal)

        ruido = np.random.normal(
            0,
            amplitud,
            len(original)
        )

        modificada = original + ruido

        return original, modificada

    def promedio(self, eje):
        return np.mean(
            self.datos_3d,
            axis=eje
        )

    def desviacion(self, eje):
        return np.std(
            self.datos_3d,
            axis=eje
        )

    def estadisticas(self, eje):
        promedio = self.promedio(eje)
        desviacion = self.desviacion(eje)

        return promedio, desviacion

    def dimensiones_3d(self):
        return self.datos_3d.shape

    def dimensiones_2d(self):
        return self.datos_2d.shape