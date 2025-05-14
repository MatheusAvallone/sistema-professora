from flask_migrate import Migrate
from app import db
import os

migrate = Migrate()

def init_db(app):
    # Remove o banco de dados existente se existir
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Banco de dados antigo removido.")

    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()
        from app.services.auth_service import AuthService
        auth_service = AuthService()
        auth_service.criar_admin_padrao()
        print("Banco de dados recriado com sucesso!")
