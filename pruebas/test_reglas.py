from datetime import datetime
from dominio.reglas import agrupar_por_tubo, calcular_fecha_envio, verificar_estabilidad

def test_agrupar_mismo_tubo_y_seccion():
    examenes = [
        {"id": "EX001", "tipo_tubo": "EDTA", "seccion": "Hematología"},
        {"id": "EX002", "tipo_tubo": "EDTA", "seccion": "Hematología"},
        {"id": "EX003", "tipo_tubo": "EDTA", "seccion": "Química"}  # Distinta sección
    ]
    grupos = agrupar_por_tubo(examenes)
    
    # Deben ser 2 grupos (Hematología+EDTA y Química+EDTA)
    assert len(grupos) == 2
    assert len(grupos["Hematología | EDTA"]) == 2

def test_agrupar_dato_faltante():
    examenes = [
        {"id": "EX008", "tipo_tubo": None, "seccion": "Química"}
    ]
    grupos = agrupar_por_tubo(examenes)
    assert "DATOS_FALTANTES" in grupos

def test_calcular_fecha_envio_antes_de_corte():
    # Extracción un Lunes a las 10:00, corte a las 14:00, despacha Lunes y Martes
    fecha_ext = datetime(2026, 10, 26, 10, 0)  # Lunes 26 de oct
    dias = ["Lunes", "Martes"]
    hora = "14:00"
    
    fecha_envio = calcular_fecha_envio(fecha_ext, dias, hora)
    assert fecha_envio.strftime("%A") == "Monday"
    assert fecha_envio.day == 26

def test_calcular_fecha_envio_despues_de_corte():
    # Extracción un Lunes a las 16:00, corte a las 14:00, despacha Lunes y Martes
    fecha_ext = datetime(2026, 10, 26, 16, 0)  # Lunes 26 de oct
    dias = ["Lunes", "Martes"]
    hora = "14:00"
    
    fecha_envio = calcular_fecha_envio(fecha_ext, dias, hora)
    assert fecha_envio.strftime("%A") == "Tuesday"
    assert fecha_envio.day == 27

def test_estabilidad_insuficiente():
    # Estabilidad 4 horas, transporte 24 horas
    assert verificar_estabilidad(4, 24) is False
    # Estabilidad 24 horas, transporte 24 horas
    assert verificar_estabilidad(24, 24) is True
    # Falta dato
    assert verificar_estabilidad(None, 24) is None
