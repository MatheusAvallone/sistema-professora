from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

# Criar a instância do SQLAlchemy antes de qualquer importação que possa usá-la
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder=os.path.abspath('templates'),
                static_folder=os.path.abspath('static'))
    
    app.config.from_object(config[config_name])
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Inicializar o SQLAlchemy com o app
    db.init_app(app)

    # Importar blueprints após a criação da instância db
    from app.controllers.auth_controller import auth_bp
    from app.controllers.painel_controller import painel_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(painel_bp)

    @app.route('/')
    def index():
        return redirect('/login')

    return app 