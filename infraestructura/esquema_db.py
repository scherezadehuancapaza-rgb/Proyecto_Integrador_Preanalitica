from infraestructura.base_datos import obtener_conexion


def crear_tablas():
    """Crea el esquema de la base de datos si no existe."""
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
