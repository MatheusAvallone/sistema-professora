from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.services.recurso_service import RecursoService
import os

recursos = Blueprint('recursos', __name__)

@recursos.route('/recursos')
@login_required
def listar():
    tipo = request.args.get('tipo')
    disciplina = request.args.get('disciplina')
    serie = request.args.get('serie')
    recursos = RecursoService.listar_recursos(
        professor_id=current_user.id,
        tipo=tipo,
        disciplina=disciplina,
        serie=serie
    )
    return render_template('recursos/listar.html', recursos=recursos)

@recursos.route('/recursos/novo', methods=['GET', 'POST'])
@login_required
def criar():
    if request.method == 'POST':
        dados = {
            'titulo': request.form['titulo'],
            'descricao': request.form.get('descricao'),
            'tipo': request.form['tipo'],
            'disciplina': request.form.get('disciplina'),
            'serie': request.form.get('serie'),
            'tags': request.form.get('tags'),
            'professor_id': current_user.id
        }
        
        if request.form.get('url'):
            dados['url'] = request.form['url']
            
        arquivo = request.files.get('arquivo')
        
        try:
            RecursoService.criar_recurso(dados, arquivo)
            flash('Recurso criado com sucesso!', 'success')
            return redirect(url_for('recursos.listar'))
        except Exception as e:
            flash(f'Erro ao criar recurso: {str(e)}', 'error')
            
    return render_template('recursos/criar.html')

@recursos.route('/recursos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    recurso = RecursoService.buscar_por_id(id)
    
    if recurso.professor_id != current_user.id:
        flash('Você não tem permissão para editar este recurso.', 'error')
        return redirect(url_for('recursos.listar'))
    
    if request.method == 'POST':
        dados = {
            'titulo': request.form['titulo'],
            'descricao': request.form.get('descricao'),
            'tipo': request.form['tipo'],
            'disciplina': request.form.get('disciplina'),
            'serie': request.form.get('serie'),
            'tags': request.form.get('tags')
        }
        
        if request.form.get('url'):
            dados['url'] = request.form['url']
            
        arquivo = request.files.get('arquivo')
        
        try:
            RecursoService.atualizar_recurso(id, dados, arquivo)
            flash('Recurso atualizado com sucesso!', 'success')
            return redirect(url_for('recursos.listar'))
        except Exception as e:
            flash(f'Erro ao atualizar recurso: {str(e)}', 'error')
            
    return render_template('recursos/editar.html', recurso=recurso)

@recursos.route('/recursos/<int:id>')
@login_required
def visualizar(id):
    recurso = RecursoService.buscar_por_id(id)
    return render_template('recursos/visualizar.html', recurso=recurso)

@recursos.route('/recursos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    recurso = RecursoService.buscar_por_id(id)
    
    if recurso.professor_id != current_user.id:
        flash('Você não tem permissão para excluir este recurso.', 'error')
        return redirect(url_for('recursos.listar'))
    
    try:
        RecursoService.excluir_recurso(id)
        flash('Recurso excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir recurso: {str(e)}', 'error')
        
    return redirect(url_for('recursos.listar'))

@recursos.route('/recursos/<int:id>/download')
@login_required
def download(id):
    recurso = RecursoService.buscar_por_id(id)
    
    if not recurso.arquivo_path or not os.path.exists(recurso.arquivo_path):
        flash('Arquivo não encontrado.', 'error')
        return redirect(url_for('recursos.visualizar', id=id))
        
    return send_file(
        recurso.arquivo_path,
        as_attachment=True,
        download_name=os.path.basename(recurso.arquivo_path)
    ) 