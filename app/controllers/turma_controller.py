from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.services.turma_service import TurmaService
from app.services.professor_service import ProfessorService

turma_bp = Blueprint('turma', __name__)
turma_service = TurmaService()
professor_service = ProfessorService()

@turma_bp.route('/turmas')
@login_required
def listar():
    turmas = turma_service.listar_todas()
    return render_template('turma/listar.html', turmas=turmas)

@turma_bp.route('/turmas/nova', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'ano': int(request.form.get('ano')),
            'periodo': request.form.get('periodo'),
            'capacidade': int(request.form.get('capacidade')) if request.form.get('capacidade') else None,
            'professor_id': int(request.form.get('professor_id')) if request.form.get('professor_id') else None,
            'horarios': []
        }

        # Processa os horários
        dias = request.form.getlist('dia_semana[]')
        horas_inicio = request.form.getlist('hora_inicio[]')
        horas_fim = request.form.getlist('hora_fim[]')

        for dia, inicio, fim in zip(dias, horas_inicio, horas_fim):
            dados['horarios'].append({
                'dia_semana': int(dia),
                'hora_inicio': inicio,
                'hora_fim': fim
            })

        # Verifica conflitos de horário
        if dados['professor_id'] and dados['horarios']:
            sem_conflito, mensagem = turma_service.verificar_conflito_horario(
                dados['professor_id'], 
                dados['horarios']
            )
            if not sem_conflito:
                flash(mensagem, 'danger')
                professores = professor_service.listar_todos()
                return render_template('turma/cadastrar.html', professores=professores)

        sucesso, resultado = turma_service.cadastrar(dados)
        
        if sucesso:
            flash('Turma cadastrada com sucesso!', 'success')
            return redirect(url_for('turma.listar'))
        else:
            flash(f'Erro ao cadastrar turma: {resultado}', 'danger')

    professores = professor_service.listar_todos()
    return render_template('turma/cadastrar.html', professores=professores)

@turma_bp.route('/turmas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    turma = turma_service.buscar_por_id(id)
    if not turma:
        flash('Turma não encontrada.', 'danger')
        return redirect(url_for('turma.listar'))

    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'ano': int(request.form.get('ano')),
            'periodo': request.form.get('periodo'),
            'capacidade': int(request.form.get('capacidade')) if request.form.get('capacidade') else None,
            'professor_id': int(request.form.get('professor_id')) if request.form.get('professor_id') else None,
            'ativa': request.form.get('ativa') == 'on',
            'horarios': []
        }

        # Processa os horários
        dias = request.form.getlist('dia_semana[]')
        horas_inicio = request.form.getlist('hora_inicio[]')
        horas_fim = request.form.getlist('hora_fim[]')

        for dia, inicio, fim in zip(dias, horas_inicio, horas_fim):
            dados['horarios'].append({
                'dia_semana': int(dia),
                'hora_inicio': inicio,
                'hora_fim': fim
            })

        # Verifica conflitos de horário
        if dados['professor_id'] and dados['horarios']:
            sem_conflito, mensagem = turma_service.verificar_conflito_horario(
                dados['professor_id'], 
                dados['horarios'],
                turma.id
            )
            if not sem_conflito:
                flash(mensagem, 'danger')
                professores = professor_service.listar_todos()
                return render_template('turma/editar.html', turma=turma, professores=professores)

        sucesso, resultado = turma_service.atualizar(id, dados)
        
        if sucesso:
            flash('Turma atualizada com sucesso!', 'success')
            return redirect(url_for('turma.listar'))
        else:
            flash(f'Erro ao atualizar turma: {resultado}', 'danger')

    professores = professor_service.listar_todos()
    return render_template('turma/editar.html', turma=turma, professores=professores)

@turma_bp.route('/turmas/excluir/<int:id>')
@login_required
def excluir(id):
    sucesso, mensagem = turma_service.excluir(id)
    
    if sucesso:
        flash('Turma excluída com sucesso!', 'success')
    else:
        flash(f'Erro ao excluir turma: {mensagem}', 'danger')
    
    return redirect(url_for('turma.listar')) 