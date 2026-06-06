import mysql.connector
from datetime import datetime


class ModeloDB:

    def __init__(self):

        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="biosync"
        )

        self.cursor = self.conexion.cursor()

    def validar_usuario(self, usuario, password):

        consulta = """
        SELECT id,nombre,rol
        FROM usuarios
        WHERE nombre=%s
        AND password=%s
        """

        self.cursor.execute(
            consulta,
            (usuario, password)
        )

        return self.cursor.fetchone()

    def guardar_sesion(self, id_usuario, ruta_foto):

        consulta = """
        INSERT INTO sesiones
        (id_usuario,ruta_foto,fecha)
        VALUES (%s,%s,%s)
        """

        self.cursor.execute(
            consulta,
            (
                id_usuario,
                ruta_foto,
                datetime.now()
            )
        )

        self.conexion.commit()

    def cerrar(self):

        self.cursor.close()
        self.conexion.close()