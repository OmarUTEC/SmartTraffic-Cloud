from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Modelo Semaforo
class Semaforo(db.Model):
    __tablename__ = 'semaforo'
    id_semaforo = db.Column(db.Integer, primary_key=True)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id_sensor'))
    id_interseccion = db.Column(db.Integer, db.ForeignKey('interseccion.interseccion_id'))
    estado_actual = db.Column(db.Boolean, nullable=False)
    ultima_actualizacion = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())

# Modelo History
class History(db.Model):
    __tablename__ = 'history'
    id_history = db.Column(db.Integer, primary_key=True)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id_sensor'))
    id_semaforo = db.Column(db.Integer, db.ForeignKey('semaforo.id_semaforo'))
    id_interseccion = db.Column(db.Integer, db.ForeignKey('interseccion.interseccion_id'))
    estado = db.Column(db.Boolean, nullable=False)
    ultima = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())

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

# Modelo Avenida_Interseccion
class AvenidaInterseccion(db.Model):
    __tablename__ = 'avenida_interseccion'
    interseccion_id = db.Column(db.Integer, db.ForeignKey('interseccion.interseccion_id'), primary_key=True)
    avenida_id = db.Column(db.Integer, db.ForeignKey('avenida.id_avenida'), primary_key=True)