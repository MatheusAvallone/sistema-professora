from flask_migrate import Migrate
from app import db
import os

migrate = Migrate()

def init_db(app):
    # Inicializa o Flask-Migrate
    migrate.init_app(app, db)
    
    with app.app_context():
        # Cria as tabelas se não existirem
        db.create_all()
        
        # Verifica se já existe um usuário admin
        from app.services.auth_service import AuthService
        auth_service = AuthService()
        
        # Cria o usuário admin apenas se não existir
        if not auth_service.verificar_admin_existe():
            auth_service.criar_admin_padrao()
            print("Usuário admin criado com sucesso!")
