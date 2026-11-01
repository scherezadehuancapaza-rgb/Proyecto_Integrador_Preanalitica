# Preanalítica - Web de Apoyo para Enfermería

Herramienta de software local desarrollada para el **Proyecto Integrador ACI** de Ingeniería en Informática y Gestión (UDP). Permite al personal de enfermería determinar los tubos de laboratorio necesarios, su orden de extracción (CLSI GP41), las condiciones preanalíticas y el destino de las muestras a partir de una lista de exámenes indicados.

> **IMPORTANTE:** Este es un prototipo local (Versión 1). Los datos clínicos utilizados actualmente son **ficticios (de prueba)** y no deben usarse para atención clínica real. Esta herramienta no reemplaza el manual de toma de muestras del laboratorio.
- Es solo un Borrador el proyecto definitivo requiere aprobacion de todo el equipo su fin es ir confirmando solo la arquitectuta a implementar y permitir mejoras.
---

## Alcance de la Versión 1
- **Incluido:** Pacientes adultos, uso en computador, búsqueda tolerante a errores, agrupación de tubos, alertas de estabilidad, derivación a laboratorios externos y auditoría anónima.
- **Fuera del alcance (Versión 2):** Cálculo de volúmenes de sangre a extraer, integración con ficha clínica electrónica (HIS), despliegue en servidor de producción y pacientes pediátricos.

---

##  Evidencia E - Arquitectura y Diseño 
El proyecto aplica los principios **SOLID** y una **Arquitectura en capas con prácticas de Código Limpio** para separar las reglas de negocio del framework web y la base de datos:

1. **Capa de Dominio (`dominio/`):** Entidades (`Examen`, `Tubo`, `ResumenToma`) y reglas de negocio puras (cálculo de fechas, agrupación). No depende de Flask ni SQLite.
2. **Capa de Aplicación (`aplicacion/`):** Orquesta los casos de uso (`ServicioBuscador`, `ServicioResumen`, `ServicioImportador`).
3. **Capa de Infraestructura (`infraestructura/`):** Persistencia (SQLite), lectura de archivos (Pandas) y envío de correos (SMTP).
4. **Capa de Interfaces (`interfaces/`):** Rutas de Flask, plantillas Jinja2 (`base.html`, `login.html`, `buscador.html`) y archivos estáticos (CSS/JS).
5. **Carpeta de Datos Locales (`datos/`):** Directorio de almacenamiento local exigido por la configuración. Aquí se guarda el archivo Excel de prueba (insumo) y, a través de la capa de infraestructura, se genera automáticamente la base de datos **`preanalitica.db`** para su uso por parte del sistema.

Preanalitica/
│
├── datos/                         # Datos de prueba (Excel)
│   └── Preanalitica_Datos_de_Prueba_Adaptado.xlsx
│
├── dominio/                       # CAPA DE DOMINIO (Reglas puras)
│   ├── __init__.py
│   ├── modelos.py                 # Dataclasses (Examen, Tubo, ResumenToma)
│   └── reglas.py                  # Lógica pura (agrupación, fechas)
│
├── aplicacion/                    # CAPA DE APLICACIÓN (Casos de uso)
│   ├── __init__.py
│   ├── servicio_buscador.py       # Búsqueda con RapidFuzz y Unidecode
│   ├── servicio_importador.py     # Lógica de importación de Excel
│   └── servicio_resumen.py        # Orquesta el resumen de tubos
│
├── infraestructura/               # CAPA DE INFRAESTRUCTURA (Conexiones externas)
│   ├── __init__.py
│   ├── base_datos.py              # Conexión a SQLite y creación de tablas
│   ├── enviador_correo.py         # Envío SMTP y tareas programadas (APScheduler)
│   ├── lector_excel.py            # Lectura del Excel con Pandas
│   └── repositorio.py             # Consultas SQL (Patrón Repository)
│
├── interfaces/                    # CAPA DE INTERFAZ (Flask Web)
│   ├── __init__.py
│   ├── rutas.py                   # Controladores/Endpoints (Blueprints)
│   │
│   ├── estaticos/                 # Archivos Frontend
│   │   ├── estilos.css            # Hoja de estilos
│   │   └── buscador.js            # Lógica de autocompletado (Fetch API)
│   │
│   └── plantillas/                # Vistas (Jinja2)
│       ├── base.html              # Plantilla base (hereda footer y head)
│       ├── login.html             # Pantalla inicial
│       ├── buscador.html          # Pantalla de búsqueda
│       └── resumen.html           # Pantalla de resumen de tubos
│
├── pruebas/                       # PRUEBAS UNITARIAS (Pytest)
│   ├── __init__.py
│   ├── test_buscador.py
│   └── test_reglas.py
│
├── app.py                         # Punto de entrada (Flask App Factory)
├── configuracion.py               # Variables de entorno y orden CLSI editable
├── importar_excel.py              # Script disparador para poblar la BD
├── enviar_reporte.py              # Script para disparar envío de auditoría manual
├── requirements.txt               # Dependencias (Flask, Pandas, Pytest, etc.)
├── .flake8                        # Configuración del linter de Código Limpio
├── .env.example                   # Plantilla de variables SMTP
├── .gitignore                     # Archivos ignorados por Git
└── README.md                      # Este documento
---

## F. Desarrollo e Integración- F.1 Stack Tecnológico
- **Backend:** Python 3.10+ / Flask
- **Base de Datos:** SQLite
- **Procesamiento de Datos:** Pandas y OpenPyXL
- **Búsqueda Difusa:** RapidFuzz y Unidecode
- **Tareas Programadas:** APScheduler y smtplib
- **Frontend:** Jinja2, HTML5, CSS3 y Vanilla JavaScript (Fetch API)
- **Calidad:** Pytest (pruebas) y Flake8 (análisis estático)
## F.2 Integración y Persistencia
La integración del listado clínico se realiza mediante el script importar_excel.py, el cual lee el archivo Excel y actualiza la base de datos SQLite sin tocar el código. La app web consume esta base de datos mediante el patrón de diseño Repository (capa de infraestructura).

## F.3 Uso de Git
Se utilizó Git para el control de versiones. Se trabajó con ramas por módulo (feature/buscador, feature/agrupacion-tubos, feature/auditoria-feature/auditoria-correo, etc.)
---
## G. Calidad y Pruebas
## G.1 Pruebas Unitarias (Pytest)
Se implementaron pruebas con pytest para asegurar la calidad de las reglas de negocio:

test_reglas.py: Valida que los exámenes se agrupen correctamente por sección y tubo, que el cálculo de la fecha de envío respete los días de despacho, y que la función de estabilidad detecte muestras inestables.

test_buscador.py: Valida que el buscador tolere errores de tipeo y acentos (ej. que "gluco" encuentre "Glicemia"). Para ello se usó unittest.mock para aislar la base de datos.

## G.2 Análisis Estático de Código (Flake8)
Para garantizar el "Código Limpio", se utilizó Flake8 bajo el estándar PEP 8. Se configuró un archivo .flake8 con un límite de 120 caracteres por línea. El proyecto finaliza con 0 errores y 0 advertencias.

## G.3 Manejo de Errores y Datos Faltantes
En línea con la regla clave de no inventar datos clínicos, si un examen no tiene tubo o estabilidad asignada en el Excel, el sistema lo captura y lo muestra en la interfaz como DATOS_FALTANTES o "Estabilidad no registrada", sin romper la aplicación.
## Evidencia H: Plan de Despliegue y Operación

### 1. Ambientes y Recursos Necesarios
Para el correcto funcionamiento del prototipo local, el equipo de TI debe preparar el siguiente ambiente:
- **Sistema Operativo:** Windows 10/11, macOS o Linux.
- **Software Base:** Python 3.10 o superior instalado y agregado al PATH del sistema.
- **Espacio en disco:** Mínimo 500 MB (para el entorno virtual y dependencias).
- **Red:** No requiere conexión a internet para funcionar localmente (solo para instalar dependencias la primera vez o para enviar correos SMTP).

### 2. Estrategia de Entrega
La entrega del software se realiza mediante un repositorio centralizado en GitHub. El código fuente, los archivos de configuración y la documentación se clonan directamente. El archivo Excel con los datos del laboratorio (ficticios para esta versión) se entrega dentro de la carpeta `datos/`.

### 3. Pasos para el Despliegue Local (Instalación)

**Paso 1: Clonar el repositorio y crear el entorno virtual**
```bash
git clone https://github.com/scherezadehuancapaza-rgb/Proyecto_Integrador_Preanalitica.git
cd Proyecto_Integrador_Preanalitica

# Crear el entorno virtual
python -m venv venv

# Activarlo en Windows:
.\venv\Scripts\activate
# Activarlo en Mac/Linux:
source venv/bin/activate