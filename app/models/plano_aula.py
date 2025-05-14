from datetime import datetime
from app import db

class PlanoAula(db.Model):
    __tablename__ = 'planos_aula'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    disciplina = db.Column(db.String(50), nullable=False)
    serie = db.Column(db.String(20), nullable=False)
    data_aula = db.Column(db.Date, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # em minutos
    objetivos = db.Column(db.Text, nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    metodologia = db.Column(db.Text, nullable=False)
    recursos = db.Column(db.Text, nullable=False)
    avaliacao = db.Column(db.Text, nullable=False)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pendente')  # Pendente, Aprovado, Revisão
    
    # Relacionamentos
    professor_id = db.Column(db.Integer, db.ForeignKey('professoras.id'), nullable=False)
    professor = db.relationship('Professor', backref='planos_aula')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PlanoAula {self.titulo}>' 