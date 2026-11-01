import smtplib
from email.message import EmailMessage
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from configuracion import SMTP_SERVIDOR, SMTP_PUERTO, SMTP_USUARIO, SMTP_CLAVE, CORREOS_DESTINO
from infraestructura.base_datos import obtener_conexion

def generar_reporte_auditoria():
    """Extrae los registros de auditoría de SQLite y crea un Excel."""
    with obtener_conexion() as conexion:
        # Asumimos que existirá una tabla auditoria (se creará más adelante en la app)
        try:
            df = pd.read_sql_query("SELECT * FROM auditoria", conexion)
        except Exception:
            print("Aún no hay tabla de auditoría o está vacía.")
            return None

    ruta_excel = "auditoria_semanal.xlsx"
    df.to_excel(ruta_excel, index=False)
    return ruta_excel

def enviar_correo_auditoria():
    """Envía el archivo Excel por correo."""
    ruta_excel = generar_reporte_auditoria()
    if not ruta_excel:
        return

    if not SMTP_SERVIDOR or not SMTP_USUARIO:
        print("SMTP no configurado. El reporte se guardó localmente.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Reporte Semanal de Uso - Preanalítica'
    msg['From'] = SMTP_USUARIO
    msg['To'] = ", ".join(CORREOS_DESTINO)
    msg.set_content('Adjunto encontrarás el reporte de uso semanal.')

    with open(ruta_excel, 'rb') as f:
        contenido = f.read()
        msg.add_attachment(contenido, maintype='application', subtype='xlsx', filename=ruta_excel)

    try:
        with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PUERTO) as server:
            server.starttls()
            server.login(SMTP_USUARIO, SMTP_CLAVE)
            server.send_message(msg)
        print("Correo enviado exitosamente.")
        # Aquí iría la lógica para borrar los registros enviados (RF-25)
    except Exception as e:
        print(f"Error al enviar correo: {e}. No se borrarán los registros.")

def iniciar_programador_tareas():
    """Inicia APScheduler para que se ejecute todos los viernes a las 18:00."""
    scheduler = BackgroundScheduler()
    # Se ejecuta todos los viernes a las 18:00
    scheduler.add_job(enviar_correo_auditoria, 'cron', day_of_week='fri', hour=18, minute=0)
    scheduler.start()
    print("Programador de tareas (APScheduler) iniciado.")
 
