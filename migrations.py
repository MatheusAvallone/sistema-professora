from flask_migrate import Migrate
from sqlalchemy import text
from app import create_app, db
from app.models.nota import Nota
from app.models.aluno import Aluno
from app.models.professor import Professor
from app.models.turma import Turma
from app.models.horario_aula import HorarioAula
from app.models.tipo_evento import TipoEvento
from app.models.evento_calendario import EventoCalendario

app = create_app()
migrate = Migrate(app, db)

def create_tables():
    """Cria todas as tabelas no banco de dados."""
    db.create_all()
    print("Tabelas criadas com sucesso!")

def drop_tables():
    """Remove todas as tabelas do banco de dados."""
    db.drop_all()
    print("Tabelas removidas com sucesso!")

def reset_tables():
    """Remove e recria todas as tabelas do banco de dados."""
    drop_tables()
    create_tables()
    print("Tabelas resetadas com sucesso!")

if __name__ == '__main__':
    with app.app_context():
        reset_tables()
        
        # Verificar se a coluna 'faltas' existe na tabela 'notas'
        with db.engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(notas)"))
            columns = [row[1] for row in result]
            
            if 'faltas' not in columns:
                # Adicionar a coluna 'faltas'
                conn.execute(text("ALTER TABLE notas ADD COLUMN faltas INTEGER DEFAULT 0"))
                conn.commit()
                print("Coluna 'faltas' adicionada com sucesso!")
            else:
                print("Coluna 'faltas' já existe!") 