from app import db
from datetime import datetime

class Nota(db.Model):
    __tablename__ = 'notas'
    
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))  # Descrição da avaliação
    data_avaliacao = db.Column(db.Date, nullable=False)
    bimestre = db.Column(db.Integer, nullable=False)  # 1, 2, 3 ou 4
    tipo_avaliacao = db.Column(db.String(50), nullable=False)  # Avaliação 1, Avaliação 2, Atividade 1, etc.
    faltas = db.Column(db.Integer, default=0)  # Número de faltas
    peso = db.Column(db.Float, default=1.0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    aluno = db.relationship('Aluno', backref=db.backref('notas', lazy=True))
    
    professor_id = db.Column(db.Integer, db.ForeignKey('professoras.id'), nullable=False)
    professor = db.relationship('Professor', backref=db.backref('notas_lancadas', lazy=True))
    
    def __repr__(self):
        return f'<Nota {self.valor} - Aluno {self.aluno_id} - Bimestre {self.bimestre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'descricao': self.descricao,
            'data_avaliacao': self.data_avaliacao.strftime('%Y-%m-%d'),
            'bimestre': self.bimestre,
            'tipo_avaliacao': self.tipo_avaliacao,
            'faltas': self.faltas,
            'peso': self.peso,
            'aluno_id': self.aluno_id,
            'aluno_nome': self.aluno.nome if self.aluno else None,
            'professor_id': self.professor_id,
            'professor_nome': self.professor.nome if self.professor else None,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        } 