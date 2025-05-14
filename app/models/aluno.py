from app import db
from datetime import datetime

class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    responsavel = db.Column(db.String(100))
    telefone_responsavel = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Aluno {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'email': self.email,
            'telefone': self.telefone,
            'responsavel': self.responsavel,
            'telefone_responsavel': self.telefone_responsavel,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        } 