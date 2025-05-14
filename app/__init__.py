from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
import os

# Criar a instância do SQLAlchemy antes de qualquer importação que possa usá-la
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(config[config_name])
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Inicializar o SQLAlchemy com o app
    db.init_app(app)
    
    # Inicializar o Flask-Migrate
    migrate.init_app(app, db)

    # Configurar o Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Importar blueprints após a criação da instância db
    from app.controllers.auth_controller import auth_bp
    from app.controllers.painel_controller import painel_bp
    from app.controllers.professor_controller import professor_bp
    from app.controllers.aluno_controller import aluno_bp
    from app.controllers.nota_controller import nota_bp
    from app.controllers.turma_controller import turma_bp
    from app.controllers.horario_controller import horario_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(painel_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(turma_bp)
    app.register_blueprint(horario_bp)

    @app.route('/')
    def index():
        return redirect('/login')

    return app 