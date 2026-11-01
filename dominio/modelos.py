from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Examen:
    id_examen: str
    nombre_examen: str
    siglas: Optional[str]
    sinonimos: Optional[str]
    seccion: str
    tipo_tubo: Optional[str]
    tubo_exclusivo: Optional[str]
    condicion_especial: Optional[str]
    ayuno: Optional[str]
    proteccion_luz: Optional[str]
    requiere_hielo: Optional[str]
    temperatura_conservacion: Optional[str]
    estabilidad_horas: Optional[float]
    destino: Optional[str]
    laboratorio_externo: Optional[str]
    volumen_requerido: Optional[float]
    unidad_volumen: Optional[str]
    advertencia_preanalitica: Optional[str]

@dataclass
class Tubo:
    tipo_tubo: str
    color_tapa: str
    aditivo: str
    orden_extraccion: int
    examenes: List[Examen] # Exámenes asignados a este tubo

@dataclass
class Alerta:
    tipo: str # AYUNO, LUZ, HIELO, ESTABILIDAD, FALTANTE
    mensaje: str

@dataclass
class ResumenToma:
    tubos_ordenados: List[Tubo]
    examenes_derivados: List[Examen]
    alertas: List[Alerta]
