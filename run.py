from flask import Flask, flash, render_template, redirect, url_for, request, session
from models.models_usuarios import db, Usuario, Administrador, Visitante
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

import datetime


app = Flask(__name__)

app.secret_key = "mys3cr3tk3y"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/smarttraffic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicializa Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
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



@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')

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
@admin_required
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





@app.route('/test_db')
def test_db():
    try:
        # Realiza una consulta sencilla
        usuarios = Usuario.query.all()
        return f"Conexión exitosa. Número de usuarios: {len(usuarios)}"
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"
    

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)
