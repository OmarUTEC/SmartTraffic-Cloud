from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime
db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Administrador(Usuario):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(10), nullable=False)
    apellidos = db.Column(db.String(40), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'administrador',
        'concrete': True
    }

class Visitante(Usuario):
    __tablename__ = 'visitante'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    ultimo_ingreso = db.Column(db.DateTime)
    __mapper_args__ = {
        'polymorphic_identity': 'visitante',
        'concrete': True
    }

    @classmethod
    def actualizar_tiempo_visitante(cls, session, visitante_id, incremento):
        visitante = Visitante.query.get(visitante_id)
        try:
            db.session.execute(
                f"SELECT incrementar_tiempo_activo({incremento},{visitante_id})"
            )
            db.session.commit()
            return f"Update - session time"
        except Exception as e:
            return f"error: {e}"


# Modelo Semaforo
class Semaforo(db.Model):
    __tablename__ = 'semaforo'
    id_semaforo = db.Column(db.Integer, primary_key=True)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id_sensor'))
    id_interseccion = db.Column(db.Integer, db.ForeignKey('interseccion.interseccion_id'))
    estado_actual = db.Column(db.Boolean, nullable=False)
    ultima_actualizacion = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    distancia = db.Column(db.Integer)
    direccion_ip = db.Column(db.String(45))

# Modelo History
class History(db.Model):
    __tablename__ = 'history'
    id_history = db.Column(db.Integer, primary_key=True)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id_sensor'))
    id_semaforo = db.Column(db.Integer, db.ForeignKey('semaforo.id_semaforo'))
    id_interseccion = db.Column(db.Integer, db.ForeignKey('interseccion.interseccion_id'))
    estado = db.Column(db.Boolean, nullable=False)
    ultima = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    distancia = db.Column(db.Integer)

# Modelo Interseccion
class Interseccion(db.Model):
    __tablename__ = 'interseccion'
    interseccion_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

# Modelo Sensor
class Sensor(db.Model):
    __tablename__ = 'sensor'
    id_sensor = db.Column(db.Integer, primary_key=True)
    modelo_sensor = db.Column(db.String(255), nullable=False)

# Modelo Avenida
class Avenida(db.Model):
    __tablename__ = 'avenida'
    id_avenida = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    carriles = db.Column(db.Integer, nullable=False)
    densidad_vial = db.Column(db.Float, nullable=False)
    hora_punta = db.Column(db.Integer, nullable=False)
    congestion = db.Column(db.Float, nullable=False)

class HistoriaAvenida(db.Model):
    __tablename__ = 'historia_avenida'
    id_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_avenida = db.Column(db.Integer, db.ForeignKey('avenida.id_avenida'), nullable=False)
    densidad_vial = db.Column(db.Float, nullable=False)
    hora = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    congestion = db.Column(db.Float, nullable=False)

# Modelo Avenida_Interseccion
class AvenidaInterseccion(db.Model):
    __tablename__ = 'avenida_interseccion'
    interseccion_id = db.Column(db.Integer, db.ForeignKey('interseccion.interseccion_id'), primary_key=True)
    avenida_id = db.Column(db.Integer, db.ForeignKey('avenida.id_avenida'), primary_key=True)
