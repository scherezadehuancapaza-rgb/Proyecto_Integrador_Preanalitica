from infraestructura.lector_excel import LectorExcel
from infraestructura.esquema_db import crear_tablas
from infraestructura.base_datos import obtener_conexion


class ServicioImportador:
    def __init__(self, ruta_excel):
        self.ruta_excel = ruta_excel
        self.lector = LectorExcel(ruta_excel)

    def ejecutar_importacion(self):
        print("Iniciando importación desde la capa de aplicación...")
        crear_tablas()

        df_tubos = self.lector.leer_hoja("Tubos")
        df_labs = self.lector.leer_hoja("Laboratorios_Externos")
        df_examenes = self.lector.leer_hoja("Examenes")

        if df_tubos is None or df_examenes is None:
            print("Error crítico: No se pudieron leer las hojas necesarias del Excel.")
            return

        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM tubos")
            cursor.execute("DELETE FROM laboratorios")
            cursor.execute("DELETE FROM examenes")

            # 1. Insertar Tubos
            for _, fila in df_tubos.iterrows():
                cursor.execute(
                    "INSERT INTO tubos (tipo_tubo, color_tapa, aditivo, orden_extraccion) "
                    "VALUES (?, ?, ?, ?)",
                    (fila['tipo_tubo'], fila['color_tapa'], fila['aditivo'], fila['orden_extraccion'])
                )

            # 2. Insertar Laboratorios (Líneas divididas para evitar E501)
            for _, fila in df_labs.iterrows():
                if fila['id_laboratorio']:
                    cursor.execute(
                        "INSERT INTO laboratorios ("
                        "id_laboratorio, nombre, dias_despacho, "
                        "hora_corte, tiempo_transporte_horas"
                        ") VALUES (?, ?, ?, ?, ?)",
                        (
                            fila['id_laboratorio'], fila['nombre_laboratorio'],
                            fila['dias_despacho'], fila['hora_corte'],
                            fila['tiempo_transporte_horas']
                        )
                    )

            # 3. Insertar Exámenes
            for _, fila in df_examenes.iterrows():
                if fila['id_examen']:
                    cursor.execute("""
                        INSERT INTO examenes (
                            id_examen, nombre_examen, siglas, sinonimos, seccion, tipo_tubo,
                            tubo_exclusivo, condicion_especial, ayuno, proteccion_luz,
                            requiere_hielo, temperatura_conservacion, estabilidad_horas,
                            destino, laboratorio_externo, volumen_requerido, unidad_volumen,
                            advertencia_preanalitica
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        fila['id_examen'], fila['nombre_examen'], fila['siglas'], fila['sinonimos'],
                        fila['seccion'], fila['tipo_tubo'], fila['tubo_exclusivo'], fila['condicion_especial'],
                        fila['ayuno'], fila['proteccion_luz'], fila['requiere_hielo'], fila['temperatura_conservacion'],
                        fila['estabilidad_horas'], fila['destino'], fila['laboratorio_externo'],
                        fila['volumen_requerido'], fila['unidad_volumen'], fila['advertencia_preanalitica']
                    ))

            conexion.commit()
        print("Importación completada con éxito. Base de datos actualizada.")
