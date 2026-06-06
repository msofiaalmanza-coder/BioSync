# BioSync

## Plataforma Integrada de Análisis Biomédico
### Integrantes

* Meilin Almanza Moreno
* Natalia Vergara Alvarez 
* Luz Adriana Doria Sanchez 
* Nicolas Villegas Restrepo 

Universidad de Antioquia
Bioingeniería
Informática II - 2026-1

## Descripción del proyecto

BioSync es una aplicación de escritorio desarrollada en Python bajo la arquitectura Modelo-Vista-Controlador (MVC), diseñada para la carga, procesamiento y análisis de diferentes tipos de datos biomédicos.

El sistema permite trabajar con:

* Imágenes médicas DICOM y NIFTI.
* Señales biomédicas almacenadas en archivos MAT.
* Datos tabulares provenientes de archivos CSV y Excel.

La aplicación integra herramientas de procesamiento, visualización y análisis en una única plataforma.


## Objetivos

* Implementar una arquitectura MVC para aplicaciones biomédicas.
* Procesar imágenes médicas en formato DICOM.
* Convertir estudios DICOM a formato NIFTI.
* Analizar señales biomédicas.
* Procesar conjuntos de datos tabulares.
* Integrar todos los módulos mediante una interfaz gráfica desarrollada en PyQt.

## Arquitectura MVC

### Modelo
Contiene la lógica de procesamiento y manejo de datos.

#### modelo_dicom.py
Permite:

* Cargar estudios DICOM.
* Reconstruir volúmenes 3D.
* Extraer metadatos.
* Convertir a unidades Hounsfield.
* Convertir DICOM a NIFTI.
* Realizar zoom.
* Aplicar segmentación.
* Aplicar operaciones morfológicas.

#### modelo_senales.py
Permite:

* Cargar señales desde archivos MAT.
* Seleccionar canales.
* Agregar ruido.
* Calcular promedio.
* Calcular desviación estándar.

#### modelo_tablas.py
Permite:

* Cargar archivos CSV y Excel.
* Obtener columnas.
* Generar información descriptiva.
* Preparar datos para gráficos y análisis.

#### modelo_db.py
Permite:

* Conectar con MySQL.
* Validar usuarios.
* Registrar sesiones.
* Almacenar información de captura de fotografías.


### Vista

Desarrollada con Qt Designer.

Interfaces:

* login.ui
* login.ui
* principal.ui


### Controlador

Gestiona la interacción entre la Vista y el Modelo.

Responsabilidades:

* Validación de usuarios.
* Captura de imágenes desde cámara.
* Gestión de eventos de interfaz.
* Comunicación con los modelos.
* Actualización de tablas y gráficos.


## Estructura del proyecto
la estructura se basa en dividirlo en 4 carpetas principales 

modelo con : modelo_dicom.py, modelo_senales.py, modelo_tablas.py, modelo_db.py

controlador con: controlador.py

vista con : main.ui, login.ui, principal.ui, vista.py, vista_login.py, vista_principal.py

y el archivo main.py, para ejecutar 


## Base de datos

en la base de datos encontramos:

Tabla usuarios y Tabla sesiones
