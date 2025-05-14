from datetime import datetime
from app import db

class Recurso(db.Model):
    __tablename__ = 'recursos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(50), nullable=False)  # documento, link, arquivo, video
    url = db.Column(db.String(255))  # para links externos
    arquivo_path = db.Column(db.String(255))  # para arquivos uploadados
    disciplina = db.Column(db.String(50))
    serie = db.Column(db.String(20))
    tags = db.Column(db.String(200))  # tags separadas por vírgula
    
    # Relacionamentos
    professor_id = db.Column(db.Integer, db.ForeignKey('professoras.id'), nullable=False)
    professor = db.relationship('Professor', backref='recursos')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Recurso {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'url': self.url,
            'arquivo_path': self.arquivo_path,
            'disciplina': self.disciplina,
            'serie': self.serie,
            'tags': self.tags,
            'professor_id': self.professor_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 