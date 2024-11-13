# app/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import Usuarios

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Recibimos los datos enviados por el cliente
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("passwords")

    # Verificamos si se proporcionaron correo y password
    if not correo or not password:
        return jsonify({"msg": "Correo y contraseña son requeridos"}), 400

    # Buscamos al usuario en la base de datos
    usuario = Usuarios.query.filter_by(correo=correo).first()

    if usuario and usuario.check_password(password):  # Verificamos la contraseña
        # Si el usuario existe y la contraseña es correcta, generamos el JWT
        access_token = create_access_token(identity={"correo": usuario.correo, "rol": usuario.cargo})
        return jsonify(access_token=access_token), 200

    # Si el correo o la contraseña son incorrectos, devolvemos un error
    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

