import os
import cv2
import pydicom
import nibabel as nib
import numpy as np
import pandas as pd
from datetime import datetime

class DicomModel:
    def __init__(self):

        self.archivos = []
        self.volumen_3d = None
        self.metadata = {}
    def cargar_dicom(self, carpeta):
        dicoms = []
        for raiz, dirs, archivos in os.walk(carpeta):
            for archivo in archivos:
                if archivo.lower().endswith(".DCM"):
                    ruta = os.path.join(raiz, archivo)
                    try:
                        ds = pydicom.dcmread(ruta)
                        dicoms.append(ds)

                    except Exception as e:
                        print(f"Error leyendo {archivo}: {e}")
        if len(dicoms) == 0:
            raise ValueError("No se encontraron archivos DICOM.")

        try:
            dicoms.sort(
                key=lambda x:float(x.ImagePositionPatient[2]))
        except Exception:
            dicoms.sort(
                key=lambda x:
                getattr(x,"InstanceNumber",0))

        self.archivos = dicoms
        self.volumen_3d = np.stack([d.pixel_array for d in dicoms])
        return self.volumen_3d

    def extraer_metadata(self):
        if len(self.archivos) == 0:
            raise ValueError("No hay estudio cargado.")
        ds = self.archivos[0]
        self.metadata = {
            "StudyDate":
                getattr(ds,"StudyDate",""),
            "StudyTime":
                getattr(ds,"StudyTime",""),
            "Modality":
                getattr(ds,"Modality",""),

            "StudyDescription":
                getattr(ds,"StudyDescription",""),

            "SeriesTime":
                getattr(ds,"SeriesTime",""),

            "Manufacturer":
                getattr(ds,"Manufacturer","")
        }

        return self.metadata

    def calcular_duracion_estudio(self):
        if not self.metadata:
            self.extraer_metadata()
        try:
            t1 = datetime.strptime(
                self.metadata["StudyTime"].split(".")[0],"%H%M%S")
            t2 = datetime.strptime(
                self.metadata["SeriesTime"].split(".")[0],"%H%M%S")
            duracion = t2 - t1
            return duracion.total_seconds()

        except Exception:
            return None

    def guardar_csv(self, ruta):
        if not self.metadata:
            self.extraer_metadata()
        datos = self.metadata.copy()
        datos["DuracionSegundos"] = (self.calcular_duracion_estudio())
        df = pd.DataFrame([datos])
        df.to_csv(ruta,index=False)

    def convertir_hu(self):
        ds = self.archivos[0]
        slope = getattr(ds,"RescaleSlope",1)
        intercept = getattr(ds,"RescaleIntercept",0)
        hu = (self.volumen_3d.astype(np.float32)* slope+ intercept)
        return hu

    def normalizar(self, imagen):
        imagen = imagen.astype(np.float32)
        minimo = np.min(imagen)
        maximo = np.max(imagen)

        if maximo == minimo:
            return np.zeros_like(imagen,dtype=np.uint8)

        imagen = ((imagen - minimo)/(maximo - minimo)) * 255

        return imagen.astype(np.uint8)

    def corte_axial(self, indice):
        indice = np.clip(indice,0,self.volumen_3d.shape[0]-1)

        return self.volumen_3d[indice,:,:]

    def corte_coronal(self, indice):
        indice = np.clip(indice, 0, self.volumen_3d.shape[1]-1)
        return self.volumen_3d[:, indice, :]

    def corte_sagital(self, indice):
        indice = np.clip(indice, 0, self.volumen_3d.shape[2]-1)
        return self.volumen_3d[:, :, indice]

    def zoom(self, imagen, x, y, ancho, alto):
        recorte = imagen[y:y+alto, x:x+ancho]
        resize = cv2.resize(recorte, (512, 512))
        return recorte, resize

    def segmentar(self, imagen, tipo, threshold=127):
        tipos = {
            "binary": cv2.THRESH_BINARY,
            "binary_inv": cv2.THRESH_BINARY_INV,
            "trunc": cv2.THRESH_TRUNC,
            "tozero": cv2.THRESH_TOZERO,
            "tozero_inv": cv2.THRESH_TOZERO_INV}

        _, resultado = cv2.threshold(
            imagen,
            threshold,
            255,
            tipos[tipo])

        return resultado

    def morfologia(self, imagen, operacion, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        operaciones = {
            "erosion": cv2.MORPH_ERODE,
            "dilatacion": cv2.MORPH_DILATE,
            "apertura": cv2.MORPH_OPEN,
            "cierre": cv2.MORPH_CLOSE,
            "gradiente": cv2.MORPH_GRADIENT}

        return cv2.morphologyEx(
            imagen,
            operaciones[operacion],
            kernel)

    def convertir_nifti(self, ruta_salida):
        nifti = nib.Nifti1Image(self.volumen_3d, np.eye(4))
        nib.save(nifti, ruta_salida)
        return ruta_salida

    def obtener_pixel_spacing(self):
        ds = self.archivos[0]
        return getattr(ds, "PixelSpacing", [1, 1])

    def obtener_slice_thickness(self):
        ds = self.archivos[0]
        return getattr(ds, "SliceThickness", 1)

    def metadata_para_tabla(self):
        if not self.metadata:
            self.extraer_metadata()

        return [
            [clave, str(valor)]
            for clave, valor in self.metadata.items()]

    def dimensiones(self):
        return self.volumen_3d.shape

    def dimensiones_mm(self, ancho_px, alto_px):
        spacing = self.obtener_pixel_spacing()
        ancho_mm = ancho_px * spacing[0]
        alto_mm = alto_px * spacing[1]
        return ancho_mm, alto_mm
