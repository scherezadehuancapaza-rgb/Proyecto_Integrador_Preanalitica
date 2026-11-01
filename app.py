from flask import Flask
from interfaces.rutas import registrar_rutas
from infraestructura.enviador_correo import iniciar_programador_tareas

def crear_app():
    # Le indicamos a Flask las carpetas exactas donde buscar los HTML y CSS/JS
    app = Flask(
        __name__, 
        template_folder='interfaces/plantillas', 
        static_folder='interfaces/estaticos'
    )
    
    # Clave secreta necesaria para que Flask maneje la sesión (nombre de la enfermera)
    app.secret_key = 'clave_super_secreta_preanalitica_2026'
    
    # Registrar las rutas (endpoints)
    registrar_rutas(app)
    
    # Iniciar APScheduler (para la HU-13 de enviar el correo semanal)
    # Nota: Si no tienes configurado el .env con el SMTP, no se caerá, 
    # solo imprimirá un mensaje en consola indicando que no hay credenciales.
    iniciar_programador_tareas()
    
    return app

if __name__ == '__main__':
    # Creamos la app y la ejecutamos en modo desarrollo
    app = crear_app()
    app.run(debug=True, port=5000)
