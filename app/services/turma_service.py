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
        """Cadastra uma nova turma com seus horários."""
        try:
            turma = Turma(
                nome=dados['nome'],
                ano=dados['ano'],
                periodo=dados['periodo'],
                capacidade=dados.get('capacidade'),
                professor_id=dados.get('professor_id'),
                ativa=True
            )
            
            # Adiciona os horários
            if 'horarios' in dados:
                for h in dados['horarios']:
                    horario = HorarioAula(
                        dia_semana=h['dia_semana'],
                        hora_inicio=time.fromisoformat(h['hora_inicio']),
                        hora_fim=time.fromisoformat(h['hora_fim'])
                    )
                    turma.horarios.append(horario)
            
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
            turma.ano = dados['ano']
            turma.periodo = dados['periodo']
            turma.capacidade = dados.get('capacidade')
            turma.professor_id = dados.get('professor_id')
            turma.ativa = dados.get('ativa', turma.ativa)

            # Atualiza os horários
            if 'horarios' in dados:
                # Remove os horários antigos
                for horario in turma.horarios:
                    db.session.delete(horario)
                
                # Adiciona os novos horários
                for h in dados['horarios']:
                    horario = HorarioAula(
                        dia_semana=h['dia_semana'],
                        hora_inicio=time.fromisoformat(h['hora_inicio']),
                        hora_fim=time.fromisoformat(h['hora_fim']),
                        turma_id=turma.id
                    )
                    db.session.add(horario)

            db.session.commit()
            return True, turma
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir(self, id):
        """Exclui uma turma e seus horários."""
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