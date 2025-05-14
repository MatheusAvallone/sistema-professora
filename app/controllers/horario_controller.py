from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.horario_aula import HorarioAula
from app.services.horario_service import HorarioService
from app.services.turma_service import TurmaService
from datetime import datetime, time

horario_bp = Blueprint('horario', __name__)
horario_service = HorarioService()
turma_service = TurmaService()

@horario_bp.route('/horarios')
@login_required
def listar():
    horarios = horario_service.listar_todos()
    return render_template('horario/listar.html', horarios=horarios)

@horario_bp.route('/horarios/novo', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        dados = {
            'dia_semana': request.form.get('dia_semana'),
            'hora_inicio': request.form.get('hora_inicio'),
            'hora_fim': request.form.get('hora_fim'),
            'turma_id': request.form.get('turma_id')
        }
        
        sucesso, resultado = horario_service.cadastrar(dados)
        
        if sucesso:
            flash('Horário cadastrado com sucesso!', 'success')
            return redirect(url_for('horario.listar'))
        else:
            flash(f'Erro ao cadastrar horário: {resultado}', 'danger')
    
    turmas = turma_service.listar_todas()
    return render_template('horario/cadastrar.html', turmas=turmas)

@horario_bp.route('/horarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    horario = horario_service.buscar_por_id(id)
    if not horario:
        flash('Horário não encontrado.', 'danger')
        return redirect(url_for('horario.listar'))

    if request.method == 'POST':
        dados = {
            'dia_semana': request.form.get('dia_semana'),
            'hora_inicio': request.form.get('hora_inicio'),
            'hora_fim': request.form.get('hora_fim'),
            'turma_id': request.form.get('turma_id')
        }
        
        sucesso, resultado = horario_service.atualizar(id, dados)
        
        if sucesso:
            flash('Horário atualizado com sucesso!', 'success')
            return redirect(url_for('horario.listar'))
        else:
            flash(f'Erro ao atualizar horário: {resultado}', 'danger')

    turmas = turma_service.listar_todas()
    return render_template('horario/editar.html', horario=horario, turmas=turmas)

@horario_bp.route('/horarios/excluir/<int:id>')
@login_required
def excluir(id):
    sucesso, mensagem = horario_service.excluir(id)
    
    if sucesso:
        flash('Horário excluído com sucesso!', 'success')
    else:
        flash(f'Erro ao excluir horário: {mensagem}', 'danger')
    
    return redirect(url_for('horario.listar')) 