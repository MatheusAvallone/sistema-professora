from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.aluno_service import AlunoService

aluno_bp = Blueprint('aluno', __name__)
aluno_service = AlunoService()

@aluno_bp.route('/alunos')
@login_required
def listar():
    alunos = aluno_service.listar_todos()
    return render_template('aluno/listar.html', alunos=alunos)

@aluno_bp.route('/alunos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'data_nascimento': request.form.get('data_nascimento'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone'),
            'responsavel': request.form.get('responsavel'),
            'telefone_responsavel': request.form.get('telefone_responsavel')
        }
        
        sucesso, resultado = aluno_service.cadastrar(dados)
        
        if sucesso:
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('aluno.listar'))
        else:
            flash(f'Erro ao cadastrar aluno: {resultado}', 'danger')
    
    return render_template('aluno/cadastrar.html')

@aluno_bp.route('/alunos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    aluno = aluno_service.buscar_por_id(id)
    if not aluno:
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('aluno.listar'))

    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'data_nascimento': request.form.get('data_nascimento'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone'),
            'responsavel': request.form.get('responsavel'),
            'telefone_responsavel': request.form.get('telefone_responsavel'),
            'ativo': request.form.get('ativo') == 'on'
        }
        
        sucesso, resultado = aluno_service.atualizar(id, dados)
        
        if sucesso:
            flash('Aluno atualizado com sucesso!', 'success')
            return redirect(url_for('aluno.listar'))
        else:
            flash(f'Erro ao atualizar aluno: {resultado}', 'danger')

    return render_template('aluno/editar.html', aluno=aluno)

@aluno_bp.route('/alunos/excluir/<int:id>')
@login_required
def excluir(id):
    sucesso, mensagem = aluno_service.excluir(id)
    
    if sucesso:
        flash('Aluno excluído com sucesso!', 'success')
    else:
        flash(f'Erro ao excluir aluno: {mensagem}', 'danger')
    
    return redirect(url_for('aluno.listar')) 