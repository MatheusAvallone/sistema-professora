from app.models.tipo_evento import TipoEvento
from app.models.evento_calendario import EventoCalendario
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from app import db

class CalendarioService:
    # Métodos para TipoEvento
    def listar_tipos_evento(self):
        """Retorna todos os tipos de evento cadastrados."""
        try:
            return TipoEvento.query.all()
        except SQLAlchemyError:
            return []

    def buscar_tipo_evento_por_id(self, id):
        """Busca um tipo de evento pelo ID."""
        try:
            return TipoEvento.query.get(id)
        except SQLAlchemyError:
            return None

    def cadastrar_tipo_evento(self, dados):
        """Cadastra um novo tipo de evento."""
        try:
            tipo = TipoEvento(
                nome=dados['nome'],
                cor=dados['cor'],
                descricao=dados.get('descricao')
            )
            
            db.session.add(tipo)
            db.session.commit()
            return True, tipo
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def atualizar_tipo_evento(self, id, dados):
        """Atualiza os dados de um tipo de evento."""
        try:
            tipo = self.buscar_tipo_evento_por_id(id)
            if not tipo:
                return False, "Tipo de evento não encontrado."

            tipo.nome = dados['nome']
            tipo.cor = dados['cor']
            tipo.descricao = dados.get('descricao', tipo.descricao)

            db.session.commit()
            return True, tipo
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir_tipo_evento(self, id):
        """Exclui um tipo de evento."""
        try:
            tipo = self.buscar_tipo_evento_por_id(id)
            if not tipo:
                return False, "Tipo de evento não encontrado."

            db.session.delete(tipo)
            db.session.commit()
            return True, "Tipo de evento excluído com sucesso."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    # Métodos para EventoCalendario
    def listar_eventos(self):
        """Retorna todos os eventos cadastrados."""
        try:
            return EventoCalendario.query.all()
        except SQLAlchemyError:
            return []

    def buscar_evento_por_id(self, id):
        """Busca um evento pelo ID."""
        try:
            return EventoCalendario.query.get(id)
        except SQLAlchemyError:
            return None

    def listar_eventos_por_mes(self, ano, mes):
        """Retorna todos os eventos de um determinado mês/ano."""
        try:
            inicio = date(ano, mes, 1)
            if mes == 12:
                fim = date(ano + 1, 1, 1)
            else:
                fim = date(ano, mes + 1, 1)
            
            return EventoCalendario.query.filter(
                (EventoCalendario.data_inicio >= inicio) &
                (EventoCalendario.data_inicio < fim)
            ).order_by(EventoCalendario.data_inicio).all()
        except SQLAlchemyError:
            return []

    def listar_proximos_eventos(self, limite=5):
        """Retorna os próximos eventos a partir da data atual."""
        try:
            agora = datetime.now()
            return EventoCalendario.query.filter(
                EventoCalendario.data_inicio >= agora
            ).order_by(EventoCalendario.data_inicio).limit(limite).all()
        except SQLAlchemyError:
            return []

    def cadastrar_evento(self, dados):
        """Cadastra um novo evento."""
        try:
            # Converte as strings de data para objetos datetime
            data_inicio = datetime.strptime(dados['data_inicio'], '%Y-%m-%dT%H:%M')
            data_fim = datetime.strptime(dados['data_fim'], '%Y-%m-%dT%H:%M')

            evento = EventoCalendario(
                titulo=dados['titulo'],
                descricao=dados.get('descricao'),
                data_inicio=data_inicio,
                data_fim=data_fim,
                local=dados.get('local'),
                publico_alvo=dados.get('publico_alvo', 'Todos'),
                status=dados.get('status', 'Agendado'),
                tipo_id=int(dados['tipo_id']),
                professor_id=int(dados['professor_id']) if dados.get('professor_id') else None
            )
            
            db.session.add(evento)
            db.session.commit()
            return True, evento
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def atualizar_evento(self, id, dados):
        """Atualiza os dados de um evento."""
        try:
            evento = self.buscar_evento_por_id(id)
            if not evento:
                return False, "Evento não encontrado."

            # Converte as strings de data para objetos datetime
            data_inicio = datetime.strptime(dados['data_inicio'], '%Y-%m-%dT%H:%M')
            data_fim = datetime.strptime(dados['data_fim'], '%Y-%m-%dT%H:%M')

            evento.titulo = dados['titulo']
            evento.descricao = dados.get('descricao', evento.descricao)
            evento.data_inicio = data_inicio
            evento.data_fim = data_fim
            evento.local = dados.get('local', evento.local)
            evento.publico_alvo = dados.get('publico_alvo', evento.publico_alvo)
            evento.status = dados.get('status', evento.status)
            evento.tipo_id = int(dados['tipo_id'])
            evento.professor_id = int(dados['professor_id']) if dados.get('professor_id') else None

            db.session.commit()
            return True, evento
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    def excluir_evento(self, id):
        """Exclui um evento."""
        try:
            evento = self.buscar_evento_por_id(id)
            if not evento:
                return False, "Evento não encontrado."

            db.session.delete(evento)
            db.session.commit()
            return True, "Evento excluído com sucesso."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e) 