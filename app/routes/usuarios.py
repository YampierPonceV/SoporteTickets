from flask import jsonify, Blueprint, request
from app.models import Usuarios
from .. import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

usuarios_bp = Blueprint('usuarios', __name__)

bcrypt = Bcrypt()

@usuarios_bp.route('/', methods=['GET'])
@jwt_required()
def get_usuarios():
    usuarios = Usuarios.query.all()
    return jsonify([{
        'id_user': u.id_user,
        'nombres': u.nombres,
        'apellido': u.apellido,
        'dni': u.dni,
        'genero':u.genero,
        'correo': u.correo,
        'cargo':u.cargo,
        'area':u.area,
        'direccion': u.direccion,
        'celular':u.celular,
        'creado': u.creado
    }for u in usuarios])

@usuarios_bp.route('/dni/<int:dni>', methods=['GET'])
@jwt_required()
def get_usuario(dni):
    user = Usuarios.query.filter_by(dni=dni).first()

    if user:
        return jsonify({
            'id_user': user.id_user,
            'nombres': user.nombres,
            'apellido': user.apellido,
            'dni': user.dni,
            'genero':user.genero,
            'correo': user.correo,
            'cargo':user.cargo,
            'area':user.area,
            'direccion': user.direccion,
            'celular':user.celular,
            'creado': user.creado
        }),200
    else:
        return jsonify({ 'message': 'Usaurio no encontrado' }), 404
    
@usuarios_bp.route('/crear_usuario', methods=['POST'])
@jwt_required()
def post_crear_usuario():
    data = request.json

    # Verificamos que todos los campos necesarios estén presentes
    if not data or 'nombres' not in data or 'apellido' not in data or 'dni' not in data or 'genero' not in data or 'correo' not in data or 'cargo' not in data or 'area' not in data or 'passwords' not in data:
        return jsonify({ 'message': 'Alguno de los campos está incompleto, asegúrate de incluir todos los campos requeridos' }), 400

    # Crear un nuevo objeto de usuario, pero no almacenar aún la contraseña
    nuevo_usuario = Usuarios(
        nombres=data['nombres'],
        apellido=data['apellido'],
        dni=data['dni'],
        genero=data['genero'],
        correo=data['correo'],
        cargo=data['cargo'],
        area=data['area'],
        direccion=data.get('direccion'),  # Usamos .get para evitar KeyError si no se incluye
        celular=data.get('celular'),  # Lo mismo para celular
    )

    # Encriptar la contraseña usando Flask-Bcrypt
    password = data['passwords']  # La contraseña que llega en la solicitud
    nuevo_usuario.set_password(password)  # Usamos el método set_password que hemos definido en el modelo

    # Añadir el nuevo usuario a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Responder con un mensaje de éxito
    return jsonify({ 'message': 'Usuario creado exitosamente', 'Usuario_DNI': nuevo_usuario.dni }), 201


@usuarios_bp.route('/soporte-ti')
def get_usuarios_ti():
    usuarios_ti = Usuarios.query.filter(Usuarios.cargo.like('SOPORTE TI')).all()

    usuarios_json = [
        {
            'id': user.id_user,
            'nombres': user.nombres,
            'apellido': user.apellido,
            'dni': user.dni,
            'genero': user.genero,
            'correo': user.correo,
            'cargo': user.cargo,
            'celular': user.celular
        }
        for user in usuarios_ti
    ]

    return jsonify(usuarios_json), 200
