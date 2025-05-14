from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.calendario_service import CalendarioService
from app.services.professor_service import ProfessorService
from app.services.turma_service import TurmaService
from datetime import datetime

calendario_bp = Blueprint('calendario', __name__)
calendario_service = CalendarioService()
professor_service = ProfessorService()
turma_service = TurmaService()

@calendario_bp.route('/calendario')
@login_required
def index():
    """Página principal do calendário."""
    tipos_evento = calendario_service.listar_tipos_evento()
    proximos_eventos = calendario_service.listar_proximos_eventos()
    return render_template('calendario/index.html', 
                         tipos_evento=tipos_evento,
                         proximos_eventos=proximos_eventos)

@calendario_bp.route('/calendario/eventos', methods=['GET'])
@login_required
def listar_eventos():
    """Retorna os eventos do mês/ano especificado."""
    try:
        mes = int(request.args.get('mes', datetime.now().month))
        ano = int(request.args.get('ano', datetime.now().year))
        eventos = calendario_service.listar_eventos_por_mes(ano, mes)
        return jsonify([evento.to_dict() for evento in eventos])
    except ValueError:
        return jsonify({'erro': 'Parâmetros inválidos'}), 400

@calendario_bp.route('/calendario/eventos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_evento():
    """Cadastra um novo evento."""
    if request.method == 'POST':
        dados = {
            'titulo': request.form.get('titulo'),
            'descricao': request.form.get('descricao'),
            'data_inicio': request.form.get('data_inicio'),
            'data_fim': request.form.get('data_fim'),
            'local': request.form.get('local'),
            'publico_alvo': request.form.get('publico_alvo'),
            'tipo_id': request.form.get('tipo_id'),
            'professor_id': current_user.id if hasattr(current_user, 'id') else None
        }
        
        sucesso, resultado = calendario_service.cadastrar_evento(dados)
        
        if sucesso:
            flash('Evento cadastrado com sucesso!', 'success')
            return redirect(url_for('calendario.index'))
        else:
            flash(f'Erro ao cadastrar evento: {resultado}', 'danger')
    
    tipos_evento = calendario_service.listar_tipos_evento()
    return render_template('calendario/cadastrar_evento.html', tipos_evento=tipos_evento)

@calendario_bp.route('/calendario/eventos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    """Edita um evento existente."""
    evento = calendario_service.buscar_evento_por_id(id)
    if not evento:
        flash('Evento não encontrado.', 'danger')
        return redirect(url_for('calendario.index'))

    if request.method == 'POST':
        dados = {
            'titulo': request.form.get('titulo'),
            'descricao': request.form.get('descricao'),
            'data_inicio': request.form.get('data_inicio'),
            'data_fim': request.form.get('data_fim'),
            'local': request.form.get('local'),
            'publico_alvo': request.form.get('publico_alvo'),
            'status': request.form.get('status'),
            'tipo_id': request.form.get('tipo_id'),
            'professor_id': evento.professor_id
        }
        
        sucesso, resultado = calendario_service.atualizar_evento(id, dados)
        
        if sucesso:
            flash('Evento atualizado com sucesso!', 'success')
            return redirect(url_for('calendario.index'))
        else:
            flash(f'Erro ao atualizar evento: {resultado}', 'danger')

    tipos_evento = calendario_service.listar_tipos_evento()
    return render_template('calendario/editar_evento.html', 
                         evento=evento,
                         tipos_evento=tipos_evento)

@calendario_bp.route('/calendario/eventos/excluir/<int:id>')
@login_required
def excluir_evento(id):
    """Exclui um evento."""
    sucesso, mensagem = calendario_service.excluir_evento(id)
    
    if sucesso:
        flash('Evento excluído com sucesso!', 'success')
    else:
        flash(f'Erro ao excluir evento: {mensagem}', 'danger')
    
    return redirect(url_for('calendario.index'))

# Rotas para Tipos de Evento
@calendario_bp.route('/calendario/tipos')
@login_required
def listar_tipos():
    """Lista todos os tipos de evento."""
    tipos = calendario_service.listar_tipos_evento()
    return render_template('calendario/tipos/listar.html', tipos=tipos)

@calendario_bp.route('/calendario/tipos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_tipo():
    """Cadastra um novo tipo de evento."""
    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'cor': request.form.get('cor'),
            'descricao': request.form.get('descricao')
        }
        
        sucesso, resultado = calendario_service.cadastrar_tipo_evento(dados)
        
        if sucesso:
            flash('Tipo de evento cadastrado com sucesso!', 'success')
            return redirect(url_for('calendario.listar_tipos'))
        else:
            flash(f'Erro ao cadastrar tipo de evento: {resultado}', 'danger')
    
    return render_template('calendario/tipos/cadastrar.html')

@calendario_bp.route('/calendario/tipos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tipo(id):
    """Edita um tipo de evento existente."""
    tipo = calendario_service.buscar_tipo_evento_por_id(id)
    if not tipo:
        flash('Tipo de evento não encontrado.', 'danger')
        return redirect(url_for('calendario.listar_tipos'))

    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'cor': request.form.get('cor'),
            'descricao': request.form.get('descricao')
        }
        
        sucesso, resultado = calendario_service.atualizar_tipo_evento(id, dados)
        
        if sucesso:
            flash('Tipo de evento atualizado com sucesso!', 'success')
            return redirect(url_for('calendario.listar_tipos'))
        else:
            flash(f'Erro ao atualizar tipo de evento: {resultado}', 'danger')

    return render_template('calendario/tipos/editar.html', tipo=tipo)

@calendario_bp.route('/calendario/tipos/excluir/<int:id>')
@login_required
def excluir_tipo(id):
    """Exclui um tipo de evento."""
    sucesso, mensagem = calendario_service.excluir_tipo_evento(id)
    
    if sucesso:
        flash('Tipo de evento excluído com sucesso!', 'success')
    else:
        flash(f'Erro ao excluir tipo de evento: {mensagem}', 'danger')
    
    return redirect(url_for('calendario.listar_tipos'))

# API para o calendário
@calendario_bp.route('/api/calendario/eventos')
@login_required
def api_eventos():
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)
    tipo_id = request.args.get('tipo_id', type=int)
    
    eventos = calendario_service.listar_eventos(mes=mes, ano=ano, tipo_id=tipo_id)
    return jsonify([evento.to_dict() for evento in eventos]) 