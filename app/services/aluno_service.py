from app.models.aluno import Aluno, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class AlunoService:
    def listar_todos(self):
        """Retorna todos os alunos cadastrados."""
        try:
            return Aluno.query.all()
        except SQLAlchemyError:
            return []

    def buscar_por_id(self, id):
        """Busca um aluno pelo ID."""
        try:
            return Aluno.query.get(id)
        except SQLAlchemyError:
            return None

    def cadastrar(self, dados):
        """Cadastra um novo aluno."""
        try:
            # Converte a string de data para objeto date
            data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
            
            aluno = Aluno(
                nome=dados['nome'],
                data_nascimento=data_nascimento,
                email=dados.get('email'),
                telefone=dados.get('telefone'),
                responsavel=dados.get('responsavel'),
                telefone_responsavel=dados.get('telefone_responsavel'),
                ativo=True
            )
            
            db.session.add(aluno)
            db.session.commit()
            return True, aluno
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def atualizar(self, id, dados):
        """Atualiza os dados de um aluno."""
        try:
            aluno = self.buscar_por_id(id)
            if not aluno:
                return False, "Aluno não encontrado."

            # Converte a string de data para objeto date
            data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
            
            aluno.nome = dados['nome']
            aluno.data_nascimento = data_nascimento
            aluno.email = dados.get('email')
            aluno.telefone = dados.get('telefone')
            aluno.responsavel = dados.get('responsavel')
            aluno.telefone_responsavel = dados.get('telefone_responsavel')
            aluno.ativo = dados.get('ativo', aluno.ativo)

            db.session.commit()
            return True, aluno
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir(self, id):
        """Exclui um aluno."""
        try:
            aluno = self.buscar_por_id(id)
            if not aluno:
                return False, "Aluno não encontrado."

            db.session.delete(aluno)
            db.session.commit()
            return True, "Aluno excluído com sucesso."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e) 