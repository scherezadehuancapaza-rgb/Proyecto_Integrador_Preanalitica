import os
from dotenv import load_dotenv

load_dotenv()

# Orden de extracción CLSI (GP41) - Editable
# Nota: El tubo SECO y SST comparten el orden 3, por lo que usamos una lista.
ORDEN_EXTRACCION_CLSI = {
    "HEMOCULTIVO": 1,
    "CITRATO": 2,
    "SECO": 3,
    "SST": 3,
    "HEPARINA": 4,
    "EDTA": 5,
    "FLUORURO": 6
}

# Configuración de correo (SMTP)
SMTP_SERVIDOR = os.getenv("SMTP_SERVIDOR", "")
SMTP_PUERTO = int(os.getenv("SMTP_PUERTO", 587))
SMTP_USUARIO = os.getenv("SMTP_USUARIO", "")
SMTP_CLAVE = os.getenv("SMTP_CLAVE", "")
CORREOS_DESTINO = os.getenv("CORREOS_DESTINO", "").split(",")
