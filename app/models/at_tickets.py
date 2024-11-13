from .. import db
from datetime import datetime

class AtencionTickets(db.Model):
    __tablename__ = 'atenciontickets'  # Nombre exacto de la tabla en la base de datos

    id_at = db.Column(db.Integer, primary_key=True)
    id_ticket = db.Column(db.Integer, db.ForeignKey('tickets.id_ticket'), nullable=False)
    id_admin = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=False)
    estado = db.Column(db.String(10), nullable=False)  # CHAR(10) en la BD
    fecha_creada = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el modelo Usuarios
    ticket = db.relationship('Tickets', back_populates='atenciontickets')
    admin = db.relationship('Usuarios', back_populates='atenciontickets')

    __table_args__ = (
        db.CheckConstraint("estado IN ('Pendiente', 'Proceso', 'Completado')", name='check_estado'),
    )

    def __repr__(self) -> str:
        return f"<Ticket {self.estado}>"