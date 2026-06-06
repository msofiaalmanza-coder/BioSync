import pymysql
from datetime import datetime

class ModeloDB:
    def __init__(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="biosync",
            port=3306
        )

    def validar_usuario(self, usuario, contrasena):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nombre, rol FROM usuarios WHERE usuario=%s AND contrasena=%s",
            (usuario, contrasena)
        )
        resultado = cursor.fetchone()
        cursor.close()
        return resultado

    def guardar_sesion(self, id_usuario, ruta_foto):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sesiones (id_usuario, ruta_foto, fecha) VALUES (%s, %s, %s)",
            (id_usuario, ruta_foto, datetime.now())
        )
        self.conn.commit()
        cursor.close()

    def cerrar(self):
        self.conn.close()