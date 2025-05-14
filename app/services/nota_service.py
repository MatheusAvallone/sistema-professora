from app.models.nota import Nota, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class NotaService:
    def listar_todas(self):
        """Retorna todas as notas cadastradas."""
        try:
            return Nota.query.all()
        except SQLAlchemyError:
            return []

    def listar_por_aluno(self, aluno_id):
        """Retorna todas as notas de um aluno específico."""
        try:
            return Nota.query.filter_by(aluno_id=aluno_id).all()
        except SQLAlchemyError:
            return []

    def listar_por_professor(self, professor_id):
        """Retorna todas as notas lançadas por um professor."""
        try:
            return Nota.query.filter_by(professor_id=professor_id).all()
        except SQLAlchemyError:
            return []

    def buscar_por_id(self, id):
        """Busca uma nota pelo ID."""
        try:
            return Nota.query.get(id)
        except SQLAlchemyError:
            return None

    def calcular_media_bimestre(self, aluno_id, bimestre):
        """Calcula a média de um aluno em um bimestre específico."""
        try:
            notas = Nota.query.filter_by(aluno_id=aluno_id, bimestre=bimestre).all()
            if not notas:
                return 0.0
            
            # Pesos específicos para cada tipo de avaliação
            pesos = {
                'Avaliação 1': 3.0,
                'Avaliação 2': 3.0,
                'Atividade 1': 1.5,
                'Atividade 2': 1.5,
                'Atividade 3': 1.0
            }
            
            soma_ponderada = 0
            soma_pesos = 0
            
            for nota in notas:
                peso = pesos.get(nota.tipo_avaliacao, 1.0)
                soma_ponderada += nota.valor * peso
                soma_pesos += peso
            
            return round(soma_ponderada / soma_pesos, 2) if soma_pesos > 0 else 0.0
        except SQLAlchemyError:
            return 0.0

    def cadastrar(self, dados):
        """Cadastra uma nova nota."""
        try:
            # Converte a string de data para objeto date
            data_avaliacao = datetime.strptime(dados['data_avaliacao'], '%Y-%m-%d').date()
            
            nota = Nota(
                valor=float(dados['valor']),
                descricao=dados.get('descricao'),
                data_avaliacao=data_avaliacao,
                bimestre=int(dados['bimestre']),
                tipo_avaliacao=dados['tipo_avaliacao'],
                peso=float(dados.get('peso', 1.0)),
                faltas=int(dados.get('faltas', 0)),
                aluno_id=int(dados['aluno_id']),
                professor_id=int(dados['professor_id'])
            )
            
            db.session.add(nota)
            db.session.commit()
            return True, nota
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def atualizar(self, id, dados):
        """Atualiza os dados de uma nota."""
        try:
            nota = self.buscar_por_id(id)
            if not nota:
                return False, "Nota não encontrada."

            # Converte a string de data para objeto date
            data_avaliacao = datetime.strptime(dados['data_avaliacao'], '%Y-%m-%d').date()
            
            nota.valor = float(dados['valor'])
            nota.descricao = dados.get('descricao')
            nota.data_avaliacao = data_avaliacao
            nota.bimestre = int(dados['bimestre'])
            nota.tipo_avaliacao = dados['tipo_avaliacao']
            nota.peso = float(dados.get('peso', nota.peso))
            nota.faltas = int(dados.get('faltas', nota.faltas))

            db.session.commit()
            return True, nota
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir(self, id):
        """Exclui uma nota."""
        try:
            nota = self.buscar_por_id(id)
            if not nota:
                return False, "Nota não encontrada."

            db.session.delete(nota)
            db.session.commit()
            return True, "Nota excluída com sucesso."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e) 