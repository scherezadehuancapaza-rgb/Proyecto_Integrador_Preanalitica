import sqlite3
import os

RUTA_BD = "datos/preanalitica.db"


def obtener_conexion():
    """Retorna una conexión a la base de datos SQLite."""
    os.makedirs(os.path.dirname(RUTA_BD), exist_ok=True)
    
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conexion
