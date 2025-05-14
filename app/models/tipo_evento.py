from app import db
from datetime import datetime

class TipoEvento(db.Model):
    __tablename__ = 'tipos_evento'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(7), nullable=False)  # Formato: #RRGGBB
    descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com eventos
    eventos = db.relationship('EventoCalendario', backref='tipo_evento', lazy=True)
    
    def __repr__(self):
        return f'<TipoEvento {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cor': self.cor,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        } 