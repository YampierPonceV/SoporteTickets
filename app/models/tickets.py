from .. import db
from datetime import datetime

class Tickets(db.Model):
    __tablename__ = 'tickets'  # Nombre exacto de la tabla en la base de datos

    id_ticket = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    prioridad = db.Column(db.String(10), nullable=False)  # CHAR(10) en la BD
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=False)
    fecha_creada = db.Column(db.DateTime, default=datetime.utcnow)
    at_ticket = db.Column(db.Boolean, default=False, nullable=False)

    # Relación con el modelo Usuarios
    usuario = db.relationship('Usuarios', back_populates='tickets')
    atenciontickets = db.relationship('AtencionTickets', back_populates='ticket')

    __table_args__ = (
        db.CheckConstraint("prioridad IN ('Moderado', 'Alto', 'Bajo')", name='check_prioridad'),
    )

    def __repr__(self) -> str:
        return f"<Ticket {self.titulo}>"
