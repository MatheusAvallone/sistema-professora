from app import db
from datetime import datetime

class EventoCalendario(db.Model):
    __tablename__ = 'eventos_calendario'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.String(200))
    publico_alvo = db.Column(db.String(100))  # Alunos, Professores, Todos, etc.
    status = db.Column(db.String(20), default='Agendado')  # Agendado, Confirmado, Cancelado, etc.
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_evento.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professoras.id'))
    professor = db.relationship('Professor', backref=db.backref('eventos_criados', lazy=True))
    
    def __repr__(self):
        return f'<EventoCalendario {self.titulo} - {self.data_inicio.strftime("%d/%m/%Y")}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data_inicio': self.data_inicio.isoformat(),
            'data_fim': self.data_fim.isoformat(),
            'local': self.local,
            'publico_alvo': self.publico_alvo,
            'status': self.status,
            'tipo_id': self.tipo_id,
            'tipo_nome': self.tipo_evento.nome if self.tipo_evento else None,
            'tipo_cor': self.tipo_evento.cor if self.tipo_evento else None,
            'professor_id': self.professor_id,
            'professor_nome': self.professor.nome if self.professor else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

    @property
    def cor(self):
        """Retorna a cor do tipo de evento."""
        return self.tipo_evento.cor if self.tipo_evento else '#000000' 