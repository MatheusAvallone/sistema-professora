from app import db
from datetime import datetime

class Turma(db.Model):
    __tablename__ = 'turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.String(20), nullable=False)  # Manhã, Tarde, Noite
    capacidade = db.Column(db.Integer)
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com professor
    professor_id = db.Column(db.Integer, db.ForeignKey('professoras.id'))
    professor = db.relationship('Professor', backref=db.backref('turmas', lazy=True))
    
    # Horários das aulas (relacionamento um-para-muitos)
    horarios = db.relationship('HorarioAula', backref='turma', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Turma {self.nome} - {self.ano}/{self.periodo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ano': self.ano,
            'periodo': self.periodo,
            'capacidade': self.capacidade,
            'ativa': self.ativa,
            'professor_id': self.professor_id,
            'professor_nome': self.professor.nome if self.professor else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        } 