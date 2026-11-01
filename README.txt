# Preanalítica - Web de Apoyo para Enfermería

Herramienta de software local desarrollada para el **Proyecto Integrador ACI** de Ingeniería en Informática y Gestión (UDP). Permite al personal de enfermería determinar los tubos de laboratorio necesarios, su orden de extracción (CLSI GP41), las condiciones preanalíticas y el destino de las muestras a partir de una lista de exámenes indicados.

> **IMPORTANTE:** Este es un prototipo local (Versión 1). Los datos clínicos utilizados actualmente son **ficticios (de prueba)** y no deben usarse para atención clínica real. Esta herramienta no reemplaza el manual de toma de muestras del laboratorio.
- Es solo un Borrador el proyecto definitivo requiere aprobacion de todo el equipo su fin es ir confirmando solo la arquitectuta a implementar y permitir mejoras.
---

## Alcance de la Versión 1
- **Incluido:** Pacientes adultos, uso en computador, búsqueda tolerante a errores, agrupación de tubos, alertas de estabilidad, derivación a laboratorios externos y auditoría anónima.
- **Fuera del alcance (Versión 2):** Cálculo de volúmenes de sangre a extraer, integración con ficha clínica electrónica (HIS), despliegue en servidor de producción y pacientes pediátricos.

---

##  Arquitectura y Diseño 
El proyecto aplica los principios **SOLID** y una **Arquitectura en capas con practicas de codigo Limpio** para separar las reglas de negocio del framework web y la base de datos:

1. **Capa de Dominio (`dominio/`):** Entidades (`Examen`, `Tubo`, `ResumenToma`) y reglas de negocio puras (cálculo de fechas, agrupación). No depende de Flask ni SQLite.
2. **Capa de Aplicación (`aplicacion/`):** Orquesta los casos de uso (`ServicioBuscador`, `ServicioResumen`, `ServicioImportador`).
3. **Capa de Infraestructura (`infraestructura/`):** Persistencia (SQLite), lectura de archivos (Pandas) y envío de correos (SMTP).
4. **Capa de Interfaces (`interfaces/`):** Rutas de Flask, plantillas Jinja2 (`base.html`, `login.html`, `buscador.html`) y archivos estáticos (CSS/JS).

---

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.10+ / Flask
- **Base de Datos:** SQLite
- **Procesamiento de Datos:** Pandas y OpenPyXL
- **Búsqueda Difusa:** RapidFuzz y Unidecode
- **Tareas Programadas:** APScheduler y smtplib
- **Frontend:** Jinja2, HTML5, CSS3 y Vanilla JavaScript (Fetch API)
- **Calidad:** Pytest (pruebas) y Flake8 (análisis estático)

---

## 🚀 Evidencia H: Plan de Despliegue y Operación

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