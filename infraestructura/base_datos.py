import sqlite3
import os

# Definimos la ruta para que se guarde dentro de la carpeta "datos"
RUTA_BD = "datos/preanalitica.db"


def obtener_conexion():
    """Retorna una conexión a la base de datos SQLite."""
    # Este bloque asegura que la carpeta "datos" exista antes de conectar
    os.makedirs(os.path.dirname(RUTA_BD), exist_ok=True)
    
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conexion


def crear_tablas():
    """Crea el esquema inicial si no existe."""
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        
        # Tabla Tubos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tubos (
                tipo_tubo TEXT PRIMARY KEY,
                color_tapa TEXT,
                aditivo TEXT,
                orden_extraccion INTEGER
            )
        """)
        
        # Tabla Laboratorios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS laboratorios (
                id_laboratorio TEXT PRIMARY KEY,
                nombre TEXT,
                dias_despacho TEXT,
                hora_corte TEXT,
                tiempo_transporte_horas REAL
            )
        """)
        
        # Tabla Examenes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS examenes (
                id_examen TEXT PRIMARY KEY,
                nombre_examen TEXT NOT NULL,
                siglas TEXT,
                sinonimos TEXT,
                seccion TEXT,
                tipo_tubo TEXT,
                tubo_exclusivo TEXT,
                condicion_especial TEXT,
                ayuno TEXT,
                proteccion_luz TEXT,
                requiere_hielo TEXT,
                temperatura_conservacion TEXT,
                estabilidad_horas REAL,
                destino TEXT,
                laboratorio_externo TEXT,
                volumen_requerido REAL,
                unidad_volumen TEXT,
                advertencia_preanalitica TEXT
            )
        """)
        
        # Tabla Auditoría
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_hora TEXT NOT NULL,
                enfermera TEXT NOT NULL,
                examenes_consultados TEXT NOT NULL,
                resultado_entregado TEXT NOT NULL
            )
        """)
        conexion.commit()
