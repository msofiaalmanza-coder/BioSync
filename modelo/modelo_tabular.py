import pandas as pd
import io


class ModeloTabular:

    def _init_(self):
        self.df = None

    def cargar(self, ruta):

        if ruta.endswith(".csv"):
            self.df = pd.read_csv(ruta)

        else:
            self.df = pd.read_excel(ruta)

        return self.df

    def get_columnas(self):
        return list(self.df.columns)

    def get_info(self):

        buffer = io.StringIO()

        self.df.info(buf=buffer)

        return buffer.getvalue()

    def get_describe(self):
        return self.df.describe()

    def get_columna(self, nombre):
        return self.df[nombre]

    def get_scatter(self, x, y):
        return self.df[x], self.df[y]

    def get_dataframe(self):
        return self.df