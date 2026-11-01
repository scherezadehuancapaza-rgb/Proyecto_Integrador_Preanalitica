from datetime import datetime
from dominio.modelos import ResumenToma, Tubo, Alerta
from dominio.reglas import agrupar_por_tubo, calcular_fecha_envio, verificar_estabilidad
from infraestructura.repositorio import Repositorio


class ServicioResumen:
    @staticmethod
    def generar_resumen(ids_examenes_seleccionados, fecha_extraccion=None):
        if not fecha_extraccion:
            fecha_extraccion = datetime.now()

        examenes = Repositorio.obtener_examenes_por_ids(ids_examenes_seleccionados)
        tubos_catalogo = {t['tipo_tubo']: t for t in Repositorio.obtener_todos_los_tubos()}
        
        # 1. Agrupar
        grupos = agrupar_por_tubo(examenes)
        
        # 2. Crear objetos Tubo y ordenarlos
        lista_tubos = []
        for clave, exs in grupos.items():
            if clave == "DATOS_FALTANTES":
                # Crear un tubo ficticio para los que no tienen tubo
                tubo_faltante = Tubo(
                    tipo_tubo="DATOS_FALTANTES",
                    color_tapa="N/A",
                    aditivo="N/A",
                    orden_extraccion=99,  # Al final
                    examenes=exs
                )
                lista_tubos.append(tubo_faltante)
            else:
                tipo_tubo_real = exs[0]['tipo_tubo']
                info_tubo = tubos_catalogo.get(tipo_tubo_real, {})
                nuevo_tubo = Tubo(
                    tipo_tubo=tipo_tubo_real,
                    color_tapa=info_tubo.get('color_tapa', 'Desconocido'),
                    aditivo=info_tubo.get('aditivo', 'Desconocido'),
                    orden_extraccion=info_tubo.get('orden_extraccion', 99),
                    examenes=exs
                )
                lista_tubos.append(nuevo_tubo)
        
        # Ordenar tubos
        lista_tubos.sort(key=lambda t: t.orden_extraccion)
        
        # 3. Generar Alertas y verificar derivaciones
        alertas = []
        derivados = []
        
        for ex in examenes:
            # Alertas básicas
            if ex.get('ayuno') == 'SI':
                msg = f"{ex['nombre_examen']} requiere ayuno."
                alertas.append(Alerta("AYUNO", msg))
                
            if ex.get('requiere_hielo') == 'SI':
                msg = f"{ex['nombre_examen']} requiere hielo."
                alertas.append(Alerta("HIELO", msg))
                
            if ex.get('proteccion_luz') == 'SI':
                msg = f"{ex['nombre_examen']} requiere protección de luz."
                alertas.append(Alerta("LUZ", msg))
            
            # Derivación
            if ex.get('destino') == 'DERIVADO':
                derivados.append(ex)
                lab = Repositorio.obtener_laboratorio(ex.get('laboratorio_externo'))
                
                if lab:
                    fecha_envio = calcular_fecha_envio(
                        fecha_extraccion, 
                        lab['dias_despacho'].split(';') if lab['dias_despacho'] else [], 
                        lab['hora_corte']
                    )
                    
                    # Guardar la fecha calculada en el examen
                    fecha_str = fecha_envio.strftime("%Y-%m-%d") if fecha_envio else "No calculable"
                    ex['fecha_envio_calculada'] = fecha_str
                    
                    # Estabilidad
                    es_estable = verificar_estabilidad(
                        ex.get('estabilidad_horas'), 
                        lab.get('tiempo_transporte_horas')
                    )
                    
                    if es_estable is False:
                        msg = f"{ex['nombre_examen']} podría no ser estable hasta llegar al laboratorio."
                        alertas.append(Alerta("ESTABILIDAD", msg))
                    elif es_estable is None:
                        msg = f"Falta dato de estabilidad o transporte para {ex['nombre_examen']}."
                        alertas.append(Alerta("FALTANTE", msg))

        return ResumenToma(
            tubos_ordenados=lista_tubos,
            examenes_derivados=derivados,
            alertas=alertas
        )
