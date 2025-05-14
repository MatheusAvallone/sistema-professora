from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.plano_aula_service import PlanoAulaService
from datetime import datetime

plano_aula = Blueprint('plano_aula', __name__)

@plano_aula.route('/planos')
@login_required
def listar():
    planos = PlanoAulaService.listar_planos(current_user.id)
    proximas_aulas = PlanoAulaService.buscar_proximas_aulas(current_user.id)
    return render_template('plano_aula/listar.html', 
                         planos=planos, 
                         proximas_aulas=proximas_aulas)

@plano_aula.route('/planos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        try:
            dados = request.form.to_dict()
            PlanoAulaService.criar_plano(dados, current_user.id)
            flash('Plano de aula criado com sucesso!', 'success')
            return redirect(url_for('plano_aula.listar'))
        except Exception as e:
            flash(f'Erro ao criar plano de aula: {str(e)}', 'danger')
    
    return render_template('plano_aula/cadastrar.html')

@plano_aula.route('/planos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    plano = PlanoAulaService.buscar_plano(id)
    
    # Verifica se o plano pertence ao professor logado
    if plano.professor_id != current_user.id:
        flash('Você não tem permissão para editar este plano de aula.', 'danger')
        return redirect(url_for('plano_aula.listar'))
    
    if request.method == 'POST':
        try:
            dados = request.form.to_dict()
            PlanoAulaService.atualizar_plano(id, dados)
            flash('Plano de aula atualizado com sucesso!', 'success')
            return redirect(url_for('plano_aula.listar'))
        except Exception as e:
            flash(f'Erro ao atualizar plano de aula: {str(e)}', 'danger')
    
    return render_template('plano_aula/editar.html', plano=plano)

@plano_aula.route('/planos/visualizar/<int:id>')
@login_required
def visualizar(id):
    plano = PlanoAulaService.buscar_plano(id)
    return render_template('plano_aula/visualizar.html', plano=plano)

@plano_aula.route('/planos/excluir/<int:id>')
@login_required
def excluir(id):
    plano = PlanoAulaService.buscar_plano(id)
    
    # Verifica se o plano pertence ao professor logado
    if plano.professor_id != current_user.id:
        flash('Você não tem permissão para excluir este plano de aula.', 'danger')
        return redirect(url_for('plano_aula.listar'))
    
    try:
        PlanoAulaService.excluir_plano(id)
        flash('Plano de aula excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir plano de aula: {str(e)}', 'danger')
    
    return redirect(url_for('plano_aula.listar'))

@plano_aula.route('/planos/status/<int:id>/<status>')
@login_required
def atualizar_status(id, status):
    plano = PlanoAulaService.buscar_plano(id)
    
    # Verifica se o plano pertence ao professor logado
    if plano.professor_id != current_user.id:
        flash('Você não tem permissão para alterar o status deste plano de aula.', 'danger')
        return redirect(url_for('plano_aula.listar'))
    
    try:
        PlanoAulaService.atualizar_status(id, status)
        flash('Status do plano de aula atualizado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar status do plano de aula: {str(e)}', 'danger')
    
    return redirect(url_for('plano_aula.listar')) 