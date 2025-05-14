from app.models.horario_aula import HorarioAula, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, time

class HorarioService:
    def listar_todos(self):
        """Retorna todos os horários cadastrados."""
        try:
            return HorarioAula.query.all()
        except SQLAlchemyError:
            return []

    def buscar_por_id(self, id):
        """Busca um horário pelo ID."""
        try:
            return HorarioAula.query.get(id)
        except SQLAlchemyError:
            return None

    def cadastrar(self, dados):
        """Cadastra um novo horário."""
        try:
            # Converte as strings de hora para objetos time
            hora_inicio = datetime.strptime(dados['hora_inicio'], '%H:%M').time()
            hora_fim = datetime.strptime(dados['hora_fim'], '%H:%M').time()

            horario = HorarioAula(
                dia_semana=int(dados['dia_semana']),
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                turma_id=int(dados['turma_id'])
            )
            
            db.session.add(horario)
            db.session.commit()
            return True, horario
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def atualizar(self, id, dados):
        """Atualiza os dados de um horário."""
        try:
            horario = self.buscar_por_id(id)
            if not horario:
                return False, "Horário não encontrado."

            # Converte as strings de hora para objetos time
            hora_inicio = datetime.strptime(dados['hora_inicio'], '%H:%M').time()
            hora_fim = datetime.strptime(dados['hora_fim'], '%H:%M').time()

            horario.dia_semana = int(dados['dia_semana'])
            horario.hora_inicio = hora_inicio
            horario.hora_fim = hora_fim
            horario.turma_id = int(dados['turma_id'])

            db.session.commit()
            return True, horario
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir(self, id):
        """Exclui um horário."""
        try:
            horario = self.buscar_por_id(id)
            if not horario:
                return False, "Horário não encontrado."

            db.session.delete(horario)
            db.session.commit()
            return True, "Horário excluído com sucesso."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e) 