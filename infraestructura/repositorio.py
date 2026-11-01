from infraestructura.base_datos import obtener_conexion

class Repositorio:
    
    @staticmethod
    def obtener_todos_los_examenes():
        """Devuelve una lista de diccionarios con todos los exámenes."""
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM examenes")
            return [dict(fila) for fila in cursor.fetchall()]

    @staticmethod
    def obtener_examenes_por_ids(ids_examenes):
        """Devuelve los exámenes que coincidan con una lista de IDs."""
        if not ids_examenes:
            return []
        
        # Creamos los marcadores de posición (?, ?, ?) para la consulta SQL
        marcadores = ",".join(["?"] * len(ids_examenes))
        consulta = f"SELECT * FROM examenes WHERE id_examen IN ({marcadores})"
        
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(consulta, ids_examenes)
            return [dict(fila) for fila in cursor.fetchall()]

    @staticmethod
    def obtener_todos_los_tubos():
        """Devuelve el catálogo de tubos."""
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM tubos")
            return [dict(fila) for fila in cursor.fetchall()]

    @staticmethod
    def obtener_laboratorio(id_laboratorio):
        """Devuelve los datos de un laboratorio externo específico."""
        if not id_laboratorio:
            return None
            
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM laboratorios WHERE id_laboratorio = ?", (id_laboratorio,))
            fila = cursor.fetchone()
            return dict(fila) if fila else None
        
    @staticmethod
    def guardar_auditoria(enfermera, examenes_consultados, resultado_entregado):
        """Guarda un registro anónimo de uso para la auditoría semanal."""
        from datetime import datetime
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO auditoria ("
                "fecha_hora, enfermera, examenes_consultados, resultado_entregado"
                ") VALUES (?, ?, ?, ?)",
                (fecha_hora, enfermera, examenes_consultados, resultado_entregado)
            )
            conexion.commit()
