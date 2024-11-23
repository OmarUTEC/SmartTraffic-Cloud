from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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



