from app import db
from app.models.recurso import Recurso
from werkzeug.utils import secure_filename
import os

class RecursoService:
    @staticmethod
    def listar_recursos(professor_id=None, tipo=None, disciplina=None, serie=None):
        query = Recurso.query
        
        if professor_id:
            query = query.filter_by(professor_id=professor_id)
        if tipo:
            query = query.filter_by(tipo=tipo)
        if disciplina:
            query = query.filter_by(disciplina=disciplina)
        if serie:
            query = query.filter_by(serie=serie)
            
        return query.order_by(Recurso.created_at.desc()).all()

    @staticmethod
    def buscar_por_id(recurso_id):
        return Recurso.query.get_or_404(recurso_id)

    @staticmethod
    def criar_recurso(dados, arquivo=None):
        recurso = Recurso(
            titulo=dados['titulo'],
            descricao=dados.get('descricao'),
            tipo=dados['tipo'],
            disciplina=dados.get('disciplina'),
            serie=dados.get('serie'),
            tags=dados.get('tags'),
            professor_id=dados['professor_id']
        )

        if dados.get('url'):
            recurso.url = dados['url']
        
        if arquivo:
            filename = secure_filename(arquivo.filename)
            # Salvar o arquivo em uma pasta específica
            arquivo_path = os.path.join('uploads', 'recursos', filename)
            os.makedirs(os.path.dirname(arquivo_path), exist_ok=True)
            arquivo.save(arquivo_path)
            recurso.arquivo_path = arquivo_path

        db.session.add(recurso)
        db.session.commit()
        return recurso

    @staticmethod
    def atualizar_recurso(recurso_id, dados, arquivo=None):
        recurso = Recurso.query.get_or_404(recurso_id)
        
        recurso.titulo = dados['titulo']
        recurso.descricao = dados.get('descricao')
        recurso.tipo = dados['tipo']
        recurso.disciplina = dados.get('disciplina')
        recurso.serie = dados.get('serie')
        recurso.tags = dados.get('tags')
        
        if dados.get('url'):
            recurso.url = dados['url']
        
        if arquivo:
            # Remover arquivo antigo se existir
            if recurso.arquivo_path and os.path.exists(recurso.arquivo_path):
                os.remove(recurso.arquivo_path)
            
            filename = secure_filename(arquivo.filename)
            arquivo_path = os.path.join('uploads', 'recursos', filename)
            os.makedirs(os.path.dirname(arquivo_path), exist_ok=True)
            arquivo.save(arquivo_path)
            recurso.arquivo_path = arquivo_path

        db.session.commit()
        return recurso

    @staticmethod
    def excluir_recurso(recurso_id):
        recurso = Recurso.query.get_or_404(recurso_id)
        
        # Remover arquivo se existir
        if recurso.arquivo_path and os.path.exists(recurso.arquivo_path):
            os.remove(recurso.arquivo_path)
            
        db.session.delete(recurso)
        db.session.commit()

    @staticmethod
    def buscar_por_tags(tags):
        """Busca recursos que contenham qualquer uma das tags fornecidas"""
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]
            
        query = Recurso.query
        for tag in tags:
            query = query.filter(Recurso.tags.like(f'%{tag}%'))
            
        return query.all() 