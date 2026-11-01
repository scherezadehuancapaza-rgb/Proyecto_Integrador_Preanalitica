
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from aplicacion.servicio_buscador import ServicioBuscador
from aplicacion.servicio_resumen import ServicioResumen
from infraestructura.repositorio import Repositorio

bp = Blueprint('main', __name__)

def registrar_rutas(app):
    app.register_blueprint(bp)

@bp.route('/')
def inicio():
    if 'enfermera' in session:
        return redirect(url_for('main.buscador'))
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    
    if not nombre or not apellido:
        return render_template('login.html', error="Nombre y apellido son obligatorios.")
    
    session['enfermera'] = f"{nombre} {apellido}"
    return redirect(url_for('main.buscador'))

@bp.route('/buscador')
def buscador():
    if 'enfermera' not in session:
        return redirect(url_for('main.inicio'))
    return render_template('buscador.html', enfermera=session['enfermera'])

@bp.route('/api/buscar')
def api_buscar():
    consulta = request.args.get('q', '')
    if not consulta:
        return jsonify([])
    
    buscador = ServicioBuscador()
    resultados = buscador.buscar(consulta)
    return jsonify(resultados)

@bp.route('/resumen', methods=['POST'])
def resumen():
    if 'enfermera' not in session:
        return redirect(url_for('main.inicio'))
        
    ids_examenes = request.form.getlist('examenes[]')
    
    servicio = ServicioResumen()
    resumen_toma = servicio.generar_resumen(ids_examenes)
    
    # --- NUEVO: Guardar Auditoría ---
    examenes_str = ", ".join(ids_examenes)
    resultado_str = ", ".join([f"Tubo {t.tipo_tubo}" for t in resumen_toma.tubos_ordenados])
    Repositorio.guardar_auditoria(session['enfermera'], examenes_str, resultado_str)
    # --------------------------------
    
    return render_template('resumen.html', resumen=resumen_toma, enfermera=session['enfermera'])

@bp.route('/nuevo_paciente')
def nuevo_paciente():
    return redirect(url_for('main.buscador'))
@bp.route('/logout')
def logout():
    session.clear()  # Borra todos los datos de la sesión
    return redirect(url_for('main.inicio'))
