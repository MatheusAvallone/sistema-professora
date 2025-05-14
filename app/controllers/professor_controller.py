from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.professor_service import ProfessorService
from app.services.auth_service import AuthService

professor_bp = Blueprint('professor', __name__)
professor_service = ProfessorService()
auth_service = AuthService()

@professor_bp.route('/professores')
@login_required
def listar():
    professores = professor_service.listar_todos()
    return render_template('professor/listar.html', professores=professores)

@professor_bp.route('/professores/novo', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone'),
            'disciplina': request.form.get('disciplina'),
            'usuario': request.form.get('usuario'),
            'senha': request.form.get('senha')
        }
        
        if auth_service.criar_professor(dados):
            flash('Professor cadastrado com sucesso!', 'success')
            return redirect(url_for('professor.listar'))
        else:
            flash('Erro ao cadastrar professor. O usuário pode já existir.', 'error')
    
    return render_template('professor/cadastrar.html')

@professor_bp.route('/professores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    professor = professor_service.buscar_por_id(id)
    
    if not professor:
        flash('Professor não encontrado.', 'error')
        return redirect(url_for('professor.listar'))
    
    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone'),
            'disciplina': request.form.get('disciplina'),
            'ativo': request.form.get('ativo') == 'on'
        }
        
        senha = request.form.get('senha')
        if senha:  # Se uma nova senha foi fornecida
            dados['senha'] = senha
        
        if professor_service.atualizar(id, dados):
            flash('Professor atualizado com sucesso!', 'success')
            return redirect(url_for('professor.listar'))
        else:
            flash('Erro ao atualizar professor.', 'error')
    
    return render_template('professor/editar.html', professor=professor)

@professor_bp.route('/professores/excluir/<int:id>')
@login_required
def excluir(id):
    if professor_service.excluir(id):
        flash('Professor excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir professor.', 'error')
    
    return redirect(url_for('professor.listar')) 