from flask import jsonify, Blueprint, request
from app.models import Tickets, Usuarios
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/', methods=['GET'])
@jwt_required()
def get_tickets():
    tickets = Tickets.query.all()
    return jsonify([{
        'id_ticket': t.id_ticket,
        'titulo': t.titulo,
        'descripcion': t.descripcion,
        'prioridad': t.prioridad,
        'at_ticket':t.at_ticket,
        'usuario': {
            'id_user': t.usuario.id_user,
            'nombres': t.usuario.nombres,
            'apellido': t.usuario.apellido,
            'cargo': t.usuario.cargo,
            'area': t.usuario.area,
            'celular': t.usuario.celular
        } if t.usuario else None  # Verifica que el usuario exista
    } for t in tickets]), 200  # Código de estado HTTP 200 para éxito

@tickets_bp.route('/id/<int:id_ticket>', methods=['GET'])
@jwt_required()
def get_ticket(id_ticket):
    ticket = Tickets.query.filter_by(id_ticket=id_ticket).first()
    if ticket:
        return jsonify({
        'id_ticket': ticket.id_ticket,
        'titulo': ticket.titulo,
        'descripcion': ticket.descripcion,
        'usuario': {
            'id_user': ticket.usuario.id_user,
            'nombres': ticket.usuario.nombres,
            'cargo': ticket.usuario.cargo,
            'area': ticket.usuario.area,
            'celular': ticket.usuario.celular
        } if ticket.usuario else None  # Verifica que el usuario exista
    }), 200
    else:
        return jsonify({ 'message' : 'Ticket no encontrado' }), 404

@tickets_bp.route('/usuario/dni/<string:dni>')
@jwt_required()
def get_user_tickets(dni):
    resultado = db.session.query(
        Tickets.titulo,
        Tickets.prioridad,
        Usuarios.nombres,
        Usuarios.cargo,
        Usuarios.area,
        Usuarios.celular
    ).join(Usuarios, Tickets.id_user == Usuarios.id_user).filter(Usuarios.dni == dni).all()

    tickets = [
        {
            'titulo': t.titulo,
            'prioridad': t.prioridad,
            'nombre': t.nombres,
            'cargo': t.cargo,
            'area': t.area,
            'celular': t.celular
        }
        for t in resultado
    ]

    return jsonify(tickets), 200

# Endpoint protegido para crear un ticket
@tickets_bp.route('/crear_ticket', methods=['POST'])
@jwt_required()  # Este decorador protege el endpoint, requiere un token JWT válido
def post_crear_ticket():
    data = request.json

    # Verificar que los campos necesarios estén presentes en la solicitud
    if not data or 'titulo' not in data or 'prioridad' not in data or 'id_user' not in data:
        return jsonify({ 'message': 'Algunos campos son obligatorios' }), 400

    # Obtener la identidad del usuario del JWT (en este caso, correo o cualquier dato de identidad que hayas pasado)
    current_user = get_jwt_identity()

    # Opcional: Verificar que el usuario exista en la base de datos antes de crear el ticket
    # Puedes hacer una consulta para verificar que el `id_user` corresponde a un usuario válido
    usuario = Usuarios.query.get(data['id_user'])
    if not usuario:
        return jsonify({ 'message': 'Usuario no encontrado' }), 404

    # Crear un nuevo ticket
    nuevo_ticket = Tickets(
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        prioridad=data['prioridad'],
        id_user=data['id_user'],
    )

    # Agregar el ticket a la base de datos y confirmar la transacción
    db.session.add(nuevo_ticket)
    db.session.commit()

    return jsonify({ 'message': 'Ticket agregado', 'id_ticket': nuevo_ticket.id_ticket }), 200


@tickets_bp.route('/sin-atender', methods=['POST'])
@jwt_required()
def get_ticket_sin_atender():
    tickes_sin_atender = Tickets.query.filter(Tickets.at_ticket.like(0)).all()

    tickes_sin_atender_json = [
        {
            'id_ticket': ticket.id_ticket,
            'titulo': ticket.titulo,
            'descripcion': ticket.id_ticket,
            'prioridad': ticket.id_ticket,
            'at_ticket': ticket.at_ticket,
            'usuario': {
            'id_user': ticket.usuario.id_user,
            'nombres': ticket.usuario.nombres,
            'cargo': ticket.usuario.cargo,
            'area': ticket.usuario.area,
            'celular': ticket.usuario.celular
        } if ticket.usuario else None
        }
        for ticket in tickes_sin_atender
    ]

    return jsonify(tickes_sin_atender_json), 200

@tickets_bp.route('/actualizar/id/<int:id_ticket>', methods=['PUT'])
@jwt_required()
def post_update_ticket(id_ticket):
    ticket = Tickets.query.get(id_ticket)

    if not ticket:
        return jsonify({'message': 'Ticket no encontrado'}), 400
    
    ticket.at_ticket = True
    
    try:
        db.session.commit()
        return jsonify({'message': 'Ticket actualazo'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ticket no actualizado', 'Error': str(e)}), 500
