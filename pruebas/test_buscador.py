
from unittest.mock import patch
from aplicacion.servicio_buscador import ServicioBuscador

# Simulamos la base de datos para no depender de SQLite en esta prueba
@patch('infraestructura.repositorio.Repositorio.obtener_todos_los_examenes')
def test_buscador_tolera_errores_y_tildes(mock_obtener):
    # Datos falsos que simulan lo que vendría del Excel
    mock_obtener.return_value = [
        {
            "id_examen": "EX016", "nombre_examen": "Glicemia",
            "siglas": "", "sinonimos": "glucosa; glicemia en sangre"
        },
        {
            "id_examen": "EX005", "nombre_examen": "Hemoglobina glicosilada",
            "siglas": "HbA1c", "sinonimos": "hemoglobina glicada; A1c"
        },
        {
            "id_examen": "EX006", "nombre_examen": "Perfil bioquímico",
            "siglas": "", "sinonimos": "bioquímica"
        }
    ]
    
    buscador = ServicioBuscador()
    
    # Caso 1: Búsqueda con error de tipeo y sin tilde ("gluco" debería encontrar Glicemia)
    resultados = buscador.buscar("gluco")
    assert len(resultados) > 0
    assert resultados[0]["id_examen"] == "EX016"
    
    # Caso 2: Buscar por sigla ("hba1c")
    resultados = buscador.buscar("hba1c")
    assert len(resultados) > 0
    assert resultados[0]["id_examen"] == "EX005"
