from app import db

class HorarioAula(db.Model):
    __tablename__ = 'horarios_aula'
    
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0 = Segunda, 1 = Terça, etc.
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    
    # Relacionamento com turma
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    
    def __repr__(self):
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        return f'<Horário {dias[self.dia_semana]} {self.hora_inicio}-{self.hora_fim}>'

    def to_dict(self):
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        return {
            'id': self.id,
            'dia_semana': self.dia_semana,
            'dia_semana_nome': dias[self.dia_semana],
            'hora_inicio': self.hora_inicio.strftime('%H:%M'),
            'hora_fim': self.hora_fim.strftime('%H:%M'),
            'turma_id': self.turma_id
        } 