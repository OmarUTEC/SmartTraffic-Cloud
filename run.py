from flask import Flask, flash, render_template, redirect, url_for, request, session, jsonify
from models.models_usuarios import *
#from models.models_traffic import db, Semaforo, History, Interseccion, Sensor, Avenida, AvenidaInterseccion, HistoriaAvenida
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
#from flask_socketio import SocketIO, emit
from flask_cors import CORS

import datetime
import random
import requests
import time
import json


app = Flask(__name__)
CORS(app)
app.secret_key = "mys3cr3tk3y"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/smarttraffic'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql:admin123@localhost:5432/pro_icc'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql:admin123@db:5432/pro_icc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#socketio = SocketIO(app, cors_allowed_origins="*")

# Inicializa Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    try:
        if session['tipo_usuario'] == "visitante":
            
            session['end_time'] = (datetime.datetime.now().hour,datetime.datetime.now().minute)
            activity_time = (session['end_time'][0]-session['start_time'][0])*60-(session['end_time'][1]-session['start_time'][1])
            try:
                Visitante.actualizar_tiempo_visitante(db.session,session['user_id'], abs(activity_time))
                print(f"Succesful updated time: with({activity_time})")
            except Exception as e:
                print(f"Error: {e}")

        logout_user()
        
        flash('Sesión cerrada.')
        return redirect(url_for('login'))
    except Exception as e:
        return f"Error: {e}", 500

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
  
        if session.get('tipo_usuario') != 'administrador':
            flash("Acceso denegado. Solo los administradores pueden acceder a esta página.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        user = Usuario.query.filter_by(correo=correo).first()
        if user and user.password == password:
            consultaAdministrador = Administrador.query.filter_by(id=user.id).first()
            consultaVisitante = Visitante.query.filter_by(id=user.id).first()
            if consultaAdministrador:
                session['user_id'] = consultaAdministrador.id
                session['tipo_usuario'] = 'administrador'
                session['nombre'] = consultaAdministrador.nombre
                session['apellidos'] = consultaAdministrador.apellidos
            elif consultaVisitante:
                session['user_id'] = consultaVisitante.id
                session['tipo_usuario'] = 'visitante'
                session['username'] = consultaVisitante.username
                session['start_time'] = (datetime.datetime.now().hour,datetime.datetime.now().minute)
                consultaVisitante.ultimo_ingreso = datetime.datetime.now()  # O el valor que desees asignar
                db.session.commit()
                
            else:
                flash('NO se pudo determinar el tipo de usuario. Problema de seguridad', 'danger')
                return render_template('login.html')

            login_user(user)  
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))  
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        #password_hash = generate_password_hash(password)
        is_admin = request.form.get('is_admin') == 'true'

        if is_admin:  
            nombre = request.form['nombre']
            apellidos = request.form['apellidos']
            telefono = request.form['telefono']
            new_admin = Administrador(correo=correo, password=password, nombre=nombre, apellidos=apellidos, telefono=telefono)
            db.session.add(new_admin)
            db.session.commit()
            
            flash('Administrador registrado correctamente.')
        else: 
            username = request.form['username']
            new_visitor = Visitante(correo=correo, password=password, username=username, ultimo_ingreso=datetime.datetime.now())
            db.session.add(new_visitor)
            db.session.commit()

            flash('Visitante registrado correctamente.')

        return redirect(url_for('login'))  

    return render_template('register.html')

@app.route('/nueva_rutina', methods=['POST'])
def nueva_rutina():
    try:
        # Obtener los datos enviados como JSON
        json_input = request.get_json().get('jsonInput', None)

        if not json_input:
            return jsonify({"success": False, "message": "No se recibió ningún contenido."}), 400

        # Convertir el string a un objeto JSON

        print("Llegue!!!!!!!!!!!!!!!")
        try:
            json_data = json.loads(json_input)
        except json.JSONDecodeError:
            return jsonify({"success": False, "message": "Contenido no es un JSON válido."}), 400

        # Empaquetar json_data dentro de un nuevo diccionario con la clave "jsonInput"
        payload = {
            "jsonInput": json.dumps(json_data)  # Convertimos json_data en un string JSON
        }
        # Hacer el POST a /recibir_json
        response = requests.post("http://localhost:5000/recibir_json", json=payload)
        print(f"Respuesta de /recibir_json: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Datos enviados correctamente."}), 200
        else:
            return jsonify({"success": False, "message": "Hubo un error al enviar los datos."}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/two-semaforos-data', methods=['GET'])
def get_two_semaforos_data():
    try:
        semaforo_ids = [1, 2]  # IDs de los semáforos que deseas mostrar
        data = {}

        for semaforo_id in semaforo_ids:
            latest_data = (
                History.query.filter_by(id_semaforo=semaforo_id)
                .order_by(History.ultima.desc())
                .limit(8)
                .all()
            )
            data[semaforo_id] = [
                {
                    'timestamp': record.ultima.isoformat(),
                    'estado': int(record.estado),
                }
                for record in latest_data
            ]

        return jsonify({'success': True, 'data': data}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/estadisticas/')
@login_required
def estadisticas():
    # Obtener los datos de la avenida con id_avenida = 1
    datos = HistoriaAvenida.query.filter_by(id_avenida=1).all()

    # Formatear los datos para Chart.js
    horas = [dato.hora.strftime("%H:%M") for dato in datos]  # Hora en formato HH:MM
    densidad_vial = [dato.densidad_vial for dato in datos]
    congestion = [dato.congestion for dato in datos]

    return render_template('estadisticas.html', horas=horas, densidad_vial=densidad_vial, congestion=congestion)

@app.route('/analisis/')
@login_required
def analisis():
    return render_template('analisis.html')

@app.route('/monitoreo/')
@login_required
def monitoreo():
    return render_template('monitoreo.html')

@app.route('/usuarios/')
@login_required
@admin_required
def usuarios():
    # Obtener la cantidad de visitantes y administradores
    cantidad_visitantes = db.session.query(Visitante).count()
    cantidad_administradores = db.session.query(Administrador).count()

    # Obtener los visitantes con su información
    visitantes = db.session.query(Visitante.username, Visitante.ultimo_ingreso, Visitante.correo).all()

    # Pasar la información al template
    return render_template('administrador_de_usuarios.html', 
                           visitantes=visitantes, 
                           cantidad_visitantes=cantidad_visitantes, 
                           cantidad_administradores=cantidad_administradores)
@app.route('/dispositivos')
@login_required
@admin_required
def dispositivos():
    return render_template('programacion_de_dispositivos.html')













#TEMPLATES ROUTES
@app.route('/avatars/')
@login_required
def avatars():
    return render_template('components/avatars.html')

@app.route('/buttons/')
@login_required
def buttons():
    return render_template('components/buttons.html')

@app.route('/gridsystem/')
@login_required
def gridsystem():
    return render_template('components/gridsystem.html')

@app.route('/panels/')
@login_required
def panels():
    return render_template('components/panels.html')

@app.route('/notifications/')
@login_required
def notifications():
    return render_template('components/notifications.html')

@app.route('/sweetalert/')
@login_required
def sweetalert():
    return render_template('components/sweetalert.html')

@app.route('/font_awesome_icons/')
@login_required
def font_awesome_icons():
    return render_template('components/font-awesome-icons.html')

@app.route('/simple_line_icons/')
@login_required
def simple_line_icons():
    return render_template('components/simple-line-icons.html')

@app.route('/typography/')
@login_required
def typography():
    return render_template('components/typography.html')

@app.route('/sidebar/')
@login_required
def sidebar():
    return render_template('sidebar-style-2.html')

@app.route('/icon_menu/')
@login_required
def icon_menu():
    return render_template('icon-menu.html')

@app.route('/forms/')
@login_required
def forms():
    return render_template('forms/forms.html')

@app.route('/tables/')
@login_required
def tables():
    return render_template('tables/tables.html')

@app.route('/datatables/')
@login_required
def datatables():
    return render_template('tables/datatables.html')

@app.route('/googlemaps/')
@login_required
def googlemaps():
    return render_template('maps/googlemaps.html')

@app.route('/jsvectormap/')
@login_required
def jsvectormap():
    return render_template('maps/jsvectormap.html')

@app.route('/charts/')
@login_required
def charts():
    return render_template('charts/charts.html')

@app.route('/sparkline/')
@login_required
def sparkline():
    return render_template('charts/sparkline.html')

@app.route('/widgets/')
@login_required
def widgets():
    return render_template('widgets.html')




@app.errorhandler(Exception)
def handle_exception(e):
    return f"Error: {str(e)}", 500
@app.route('/check_db')
def test_db():
    try:
        # Realiza una consulta sencilla
        usuarios = Usuario.query.all()
        return f"Conexión exitosa. Número de usuarios: {len(usuarios)}"
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)

