from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)

    db.init_app(app)
    
    #Configuracion de JWT
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

    jwt = JWTManager(app)

    from .routes.usuarios import usuarios_bp
    from .routes.tickets import tickets_bp
    from .routes.at_tickets import at_tickets_bp 
    from .routes.auth import auth_bp 
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
    app.register_blueprint(at_tickets_bp, url_prefix='/api/atenciontickets')
    app.register_blueprint(auth_bp, url_prefix='/')
    
    return app

    