from datetime import datetime, timedelta

def agrupar_por_tubo(examenes):
    """
    Agrupa los exámenes por tipo de tubo. 
    Regla: Solo se agrupan si son de la misma sección y del mismo tipo de tubo.
    """
    grupos = {}
    for examen in examenes:
        tipo_tubo = examen.get("tipo_tubo")
        seccion = examen.get("seccion")
        
        # Si no tiene tubo (dato faltante), va a un grupo especial
        if not tipo_tubo:
            clave = "DATOS_FALTANTES"
        else:
            # La clave de agrupación es la combinación de sección y tubo
            clave = f"{seccion} | {tipo_tubo}"
            
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(examen)
        
    return grupos

def calcular_fecha_envio(fecha_extraccion, dias_despacho, hora_corte):
    """
    Calcula la próxima fecha de envío según los días de despacho del laboratorio.
    fecha_extraccion: objeto datetime
    dias_despacho: lista de strings ej. ["Lunes", "Miércoles"]
    hora_corte: string ej. "14:00"
    """
    if not dias_despacho or not hora_corte:
        return None
        
    dias_semana = {
        "Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3, 
        "Viernes": 4, "Sábado": 5, "Domingo": 6
    }
    
    # Convertimos los días permitidos a números (0-6)
    dias_permitidos = [dias_semana[d.strip()] for d in dias_despacho if d.strip() in dias_semana]
    if not dias_permitidos:
        return None

    hora_corte_dt = datetime.strptime(hora_corte, "%H:%M").time()
    
    # Si la extracción fue antes de la hora de corte del mismo día, se envía hoy
    # Si fue después, se busca el siguiente día permitido
    fecha_evaluar = fecha_extraccion
    
    if fecha_evaluar.time() > hora_corte_dt:
        fecha_evaluar += timedelta(days=1)
        
    # Buscamos el próximo día permitido
    while fecha_evaluar.weekday() not in dias_permitidos:
        fecha_evaluar += timedelta(days=1)
        
    return fecha_evaluar.date()

def verificar_estabilidad(estabilidad_horas, tiempo_transporte_horas):
    """
    Retorna True si la muestra es estable hasta llegar al destino.
    Retorna False si el tiempo de transporte supera la estabilidad.
    Retorna None si falta algún dato.
    """
    if estabilidad_horas is None or tiempo_transporte_horas is None:
        return None
        
    return estabilidad_horas >= tiempo_transporte_horas
