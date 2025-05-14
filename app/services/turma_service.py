from app.models.turma import Turma, db
from app.models.horario_aula import HorarioAula
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, time

class TurmaService:
    def listar_todas(self):
        """Retorna todas as turmas cadastradas."""
        try:
            return Turma.query.all()
        except SQLAlchemyError:
            return []

    def buscar_por_id(self, id):
        """Busca uma turma pelo ID."""
        try:
            return Turma.query.get(id)
        except SQLAlchemyError:
            return None

    def cadastrar(self, dados):
        """Cadastra uma nova turma."""
        try:
            turma = Turma(
                nome=dados['nome'],
                ano=int(dados['ano']),
                periodo=dados['periodo'],
                capacidade=int(dados['capacidade']) if dados['capacidade'] else None,
                professor_id=int(dados['professor_id']) if dados['professor_id'] else None
            )
            
            db.session.add(turma)
            db.session.commit()
            return True, turma
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def atualizar(self, id, dados):
        """Atualiza os dados de uma turma."""
        try:
            turma = self.buscar_por_id(id)
            if not turma:
                return False, "Turma não encontrada."

            turma.nome = dados['nome']
            turma.ano = int(dados['ano'])
            turma.periodo = dados['periodo']
            turma.capacidade = int(dados['capacidade']) if dados['capacidade'] else None
            turma.professor_id = int(dados['professor_id']) if dados['professor_id'] else None
            turma.ativa = dados['ativa']

            db.session.commit()
            return True, turma
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir(self, id):
        """Exclui uma turma."""
        try:
            turma = self.buscar_por_id(id)
            if not turma:
                return False, "Turma não encontrada."

            db.session.delete(turma)
            db.session.commit()
            return True, "Turma excluída com sucesso."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def verificar_conflito_horario(self, professor_id, horarios, turma_id=None):
        """Verifica se há conflito de horário para o professor."""
        try:
            for horario_novo in horarios:
                # Converte as strings de hora para objetos time
                hora_inicio_nova = time.fromisoformat(horario_novo['hora_inicio'])
                hora_fim_nova = time.fromisoformat(horario_novo['hora_fim'])
                dia_semana_novo = horario_novo['dia_semana']

                # Busca todas as turmas do professor
                query = Turma.query.filter_by(professor_id=professor_id)
                if turma_id:  # Exclui a turma atual em caso de edição
                    query = query.filter(Turma.id != turma_id)
                
                turmas_professor = query.all()

                for turma in turmas_professor:
                    for horario_existente in turma.horarios:
                        # Verifica se é o mesmo dia da semana
                        if horario_existente.dia_semana == dia_semana_novo:
                            # Verifica sobreposição de horários
                            if (hora_inicio_nova < horario_existente.hora_fim and
                                hora_fim_nova > horario_existente.hora_inicio):
                                return False, f"Conflito de horário com a turma {turma.nome}"

            return True, "Sem conflitos de horário"
        except Exception as e:
            return False, str(e) 