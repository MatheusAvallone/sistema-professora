from app.models.professor import Professor, db
from sqlalchemy.exc import SQLAlchemyError

class ProfessorService:
    def listar_todos(self):
        """Retorna todos os professores cadastrados."""
        try:
            return Professor.query.all()
        except SQLAlchemyError:
            return []

    def buscar_por_id(self, id):
        """Busca um professor pelo ID."""
        try:
            return Professor.query.get(id)
        except SQLAlchemyError:
            return None

    def cadastrar(self, dados):
        """Cadastra um novo professor."""
        try:
            professor = Professor(
                nome=dados['nome'],
                email=dados['email'],
                telefone=dados['telefone'],
                disciplina=dados['disciplina']
            )
            
            db.session.add(professor)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def atualizar(self, id, dados):
        """Atualiza os dados de um professor."""
        try:
            professor = self.buscar_por_id(id)
            if not professor:
                return False

            professor.nome = dados['nome']
            professor.email = dados['email']
            professor.telefone = dados['telefone']
            professor.disciplina = dados['disciplina']
            professor.ativo = dados.get('ativo', True)

            if 'senha' in dados and dados['senha']:
                professor.set_senha(dados['senha'])

            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def excluir(self, id):
        """Exclui um professor."""
        try:
            professor = self.buscar_por_id(id)
            if not professor:
                return False

            db.session.delete(professor)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False 