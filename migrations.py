from flask_migrate import Migrate
from sqlalchemy import text
from app import create_app, db
from app.models.nota import Nota
from app.models.aluno import Aluno
from app.models.professor import Professor
from app.models.turma import Turma
from app.models.horario_aula import HorarioAula

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Criar todas as tabelas se não existirem
        db.create_all()
        
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