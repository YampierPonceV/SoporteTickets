""" import secrets
print(secrets.token_hex(32))
 """

""" import bcrypt

# Contraseña en texto plano
password = "YPti23$$"

# Generar un salt (valor aleatorio usado para aumentar la seguridad del hash)
salt = bcrypt.gensalt()

# Encriptar la contraseña
hashed_password = bcrypt.hashpw(password.encode(), salt)

print("Contraseña encriptada:", hashed_password) """
