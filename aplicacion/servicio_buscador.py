from rapidfuzz import process, fuzz
from unidecode import unidecode
from infraestructura.repositorio import Repositorio

class ServicioBuscador:
    def __init__(self):
        self.examenes = Repositorio.obtener_todos_los_examenes()
        self._preparar_indice()

    def _normalizar(self, texto):
        if not texto:
            return ""
        return unidecode(str(texto)).lower().strip()

    def _preparar_indice(self):
        # Crear un diccionario de busqueda: {id_examen: "nombre siglas sinonimos"}
        self.indice = {}
        for ex in self.examenes:
            texto_busqueda = f"{ex['nombre_examen']} {ex['siglas'] or ''} {ex['sinonimos'] or ''}"
            self.indice[ex['id_examen']] = self._normalizar(texto_busqueda)

    def buscar(self, consulta, limite=5):
        consulta_norm = self._normalizar(consulta)
        if not consulta_norm:
            return []
        
        # Usar rapidfuzz para encontrar los mejores matches
        resultados = process.extract(
            consulta_norm, 
            self.indice, 
            scorer=fuzz.partial_ratio, # partial_ratio es bueno para "gluco" -> "glicemia"
            limit=limite
        )
        
        # resultados es una lista de tuplas: (id_examen, score, key)
        # Devolver los objetos examen completos
        ids_encontrados = [res[2] for res in resultados if res[1] > 60] # Umbral de similitud
        return [ex for ex in self.examenes if ex['id_examen'] in ids_encontrados]
