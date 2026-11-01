
import pandas as pd

class LectorExcel:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def leer_hoja(self, nombre_hoja):
        """Lee una hoja del Excel y reemplaza los valores NaN por None."""
        try:
            df = pd.read_excel(self.ruta_archivo, sheet_name=nombre_hoja)
            # Reemplazar NaN por None para SQLite
            return df.where(pd.notnull(df), None)
        except Exception as e:
            print(f"Error al leer la hoja {nombre_hoja}: {e}")
            return None
