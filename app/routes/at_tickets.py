from flask import jsonify, Blueprint
from app.models import Tickets, Usuarios, AtencionTickets
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db

at_tickets_bp = Blueprint('at_tickets', __name__)

@at_tickets_bp.route('/', methods=['GET'])
@jwt_required()
def get_at_tickets():

    u1 = db.aliased(Usuarios)
    u2 = db.aliased(Usuarios)

    at_tickets = db.session.query(
        Tickets.titulo,
        Tickets.prioridad,
        u2.nombres.label('nombre_usuario'),
        u2.cargo.label('cargo_usuario'),
        u2.celular.label('celular_usuario'),
        AtencionTickets.estado,
        u1.nombres.label('at_admin')
    ).join(AtencionTickets, AtencionTickets.id_ticket == Tickets.id_ticket) \
    .join(u1, u1.id_user == AtencionTickets.id_admin) \
    .join(u2, u2.id_user == Tickets.id_user) \
    .all()

    at_tickets_info = [
        {
            'titulo': at.titulo,
            'prioridad': at.prioridad,
            'nombre_usuario': at.nombre_usuario,
            'cargo_usuario': at.cargo_usuario,
            'celular_usuario': at.celular_usuario,
            'estado': at.estado,
            'at_admin': at.at_admin,
        }
        for at in at_tickets
    ]

    return jsonify(at_tickets_info), 200