from flask import Flask
from interfaces.rutas import registrar_rutas
from infraestructura.enviador_correo import iniciar_programador_tareas
from configuracion import CLAVE_SECRETA  


def crear_app():
    app = Flask(
        __name__, 
        template_folder='interfaces/plantillas', 
        static_folder='interfaces/estaticos'
    )
    
    # Usamos la clave importada, ya no está escrita en el código
    app.secret_key = CLAVE_SECRETA
    
    registrar_rutas(app)
    iniciar_programador_tareas()
    
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True, port=5000)
