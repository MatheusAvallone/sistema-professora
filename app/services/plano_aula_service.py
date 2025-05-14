from datetime import datetime
from app import db
from app.models.plano_aula import PlanoAula

class PlanoAulaService:
    @staticmethod
    def listar_planos(professor_id=None):
        """Lista todos os planos de aula, opcionalmente filtrados por professor"""
        query = PlanoAula.query
        if professor_id:
            query = query.filter_by(professor_id=professor_id)
        return query.order_by(PlanoAula.data_aula.desc()).all()
    
    @staticmethod
    def buscar_plano(id):
        """Busca um plano de aula específico"""
        return PlanoAula.query.get_or_404(id)
    
    @staticmethod
    def criar_plano(dados, professor_id):
        """Cria um novo plano de aula"""
        plano = PlanoAula(
            titulo=dados['titulo'],
            disciplina=dados['disciplina'],
            serie=dados['serie'],
            data_aula=datetime.strptime(dados['data_aula'], '%Y-%m-%d').date(),
            duracao=int(dados['duracao']),
            objetivos=dados['objetivos'],
            conteudo=dados['conteudo'],
            metodologia=dados['metodologia'],
            recursos=dados['recursos'],
            avaliacao=dados['avaliacao'],
            observacoes=dados.get('observacoes'),
            professor_id=professor_id
        )
        db.session.add(plano)
        db.session.commit()
        return plano
    
    @staticmethod
    def atualizar_plano(id, dados):
        """Atualiza um plano de aula existente"""
        plano = PlanoAula.query.get_or_404(id)
        
        plano.titulo = dados['titulo']
        plano.disciplina = dados['disciplina']
        plano.serie = dados['serie']
        plano.data_aula = datetime.strptime(dados['data_aula'], '%Y-%m-%d').date()
        plano.duracao = int(dados['duracao'])
        plano.objetivos = dados['objetivos']
        plano.conteudo = dados['conteudo']
        plano.metodologia = dados['metodologia']
        plano.recursos = dados['recursos']
        plano.avaliacao = dados['avaliacao']
        plano.observacoes = dados.get('observacoes')
        
        db.session.commit()
        return plano
    
    @staticmethod
    def excluir_plano(id):
        """Exclui um plano de aula"""
        plano = PlanoAula.query.get_or_404(id)
        db.session.delete(plano)
        db.session.commit()
    
    @staticmethod
    def atualizar_status(id, status):
        """Atualiza o status de um plano de aula"""
        plano = PlanoAula.query.get_or_404(id)
        plano.status = status
        db.session.commit()
        return plano
    
    @staticmethod
    def buscar_por_periodo(data_inicio, data_fim, professor_id=None):
        """Busca planos de aula em um período específico"""
        query = PlanoAula.query.filter(
            PlanoAula.data_aula.between(data_inicio, data_fim)
        )
        if professor_id:
            query = query.filter_by(professor_id=professor_id)
        return query.order_by(PlanoAula.data_aula).all()
    
    @staticmethod
    def buscar_proximas_aulas(professor_id=None, limite=5):
        """Busca as próximas aulas planejadas"""
        hoje = datetime.now().date()
        query = PlanoAula.query.filter(PlanoAula.data_aula >= hoje)
        if professor_id:
            query = query.filter_by(professor_id=professor_id)
        return query.order_by(PlanoAula.data_aula).limit(limite).all() 