from .. import db
from datetime import datetime
from flask_bcrypt import Bcrypt

# Instanciamos Bcrypt si aún no lo has hecho en tu __init__.py
bcrypt = Bcrypt()

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False, unique=True)
    genero = db.Column(db.String(1), nullable=False)
    correo = db.Column(db.String(50), nullable=False, unique=True)
    cargo = db.Column(db.String(20), nullable=False)
    area = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(100))
    celular = db.Column(db.String(9))
    creado = db.Column(db.DateTime, default=datetime.utcnow)
    passwords = db.Column(db.String(255), nullable=False)

    tickets = db.relationship('Tickets', back_populates='usuario')
    atenciontickets = db.relationship('AtencionTickets', back_populates='admin')

    # Restricciones personalizadas para los campos
    __table_args__ = (
        db.CheckConstraint("genero IN ('M', 'F')", name='check_genero'),
        db.CheckConstraint("length(dni) = 8 AND dni ~ '^[0-9]+$'", name='check_dni'),
        db.CheckConstraint("length(celular) = 9 AND celular ~ '^[0-9]+$'", name='check_celular'),
        db.CheckConstraint("correo LIKE '%@%.%'", name='check_correo'),
    )

    # Métodos de contraseña con Flask-Bcrypt
    def set_password(self, password):
        # Usamos Flask-Bcrypt para generar el hash de la contraseña
        self.passwords = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Usamos Flask-Bcrypt para verificar si la contraseña es correcta
        return bcrypt.check_password_hash(self.passwords, password)

    def __repr__(self):
        return f'<Usuario {self.nombres} {self.apellido}>'
