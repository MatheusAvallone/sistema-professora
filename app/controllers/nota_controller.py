from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.nota_service import NotaService
from app.services.aluno_service import AlunoService

nota_bp = Blueprint('nota', __name__)
nota_service = NotaService()
aluno_service = AlunoService()

@nota_bp.route('/notas')
@login_required
def listar():
    # Se for admin, mostra todas as notas
    if current_user.usuario == 'admin':
        notas = nota_service.listar_todas()
    else:
        # Se for professor, mostra apenas as notas que ele lançou
        notas = nota_service.listar_por_professor(current_user.id)
    
    return render_template('nota/listar.html', notas=notas)

@nota_bp.route('/notas/aluno/<int:aluno_id>')
@login_required
def listar_por_aluno(aluno_id):
    aluno = aluno_service.buscar_por_id(aluno_id)
    if not aluno:
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('nota.listar'))
    
    notas = nota_service.listar_por_aluno(aluno_id)
    
    # Calcula médias por bimestre
    medias = {
        1: nota_service.calcular_media_bimestre(aluno_id, 1),
        2: nota_service.calcular_media_bimestre(aluno_id, 2),
        3: nota_service.calcular_media_bimestre(aluno_id, 3),
        4: nota_service.calcular_media_bimestre(aluno_id, 4)
    }
    
    # Calcula total de faltas
    total_faltas = sum(nota.faltas for nota in notas)
    
    return render_template('nota/listar_aluno.html', 
                         aluno=aluno, 
                         notas=notas, 
                         medias=medias,
                         total_faltas=total_faltas)

@nota_bp.route('/notas/nova', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        dados = {
            'valor': request.form.get('valor'),
            'descricao': request.form.get('descricao'),
            'data_avaliacao': request.form.get('data_avaliacao'),
            'bimestre': request.form.get('bimestre'),
            'tipo_avaliacao': request.form.get('tipo_avaliacao'),
            'peso': request.form.get('peso', 1.0),
            'faltas': request.form.get('faltas', 0),
            'aluno_id': request.form.get('aluno_id'),
            'professor_id': current_user.id
        }
        
        sucesso, resultado = nota_service.cadastrar(dados)
        
        if sucesso:
            flash('Nota cadastrada com sucesso!', 'success')
            return redirect(url_for('nota.listar_por_aluno', aluno_id=dados['aluno_id']))
        else:
            flash(f'Erro ao cadastrar nota: {resultado}', 'danger')
    
    alunos = aluno_service.listar_todos()
    return render_template('nota/cadastrar.html', alunos=alunos)

@nota_bp.route('/notas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    nota = nota_service.buscar_por_id(id)
    if not nota:
        flash('Nota não encontrada.', 'danger')
        return redirect(url_for('nota.listar'))

    # Verifica se o usuário tem permissão para editar a nota
    if not current_user.usuario == 'admin' and nota.professor_id != current_user.id:
        flash('Você não tem permissão para editar esta nota.', 'danger')
        return redirect(url_for('nota.listar'))

    if request.method == 'POST':
        dados = {
            'valor': request.form.get('valor'),
            'descricao': request.form.get('descricao'),
            'data_avaliacao': request.form.get('data_avaliacao'),
            'bimestre': request.form.get('bimestre'),
            'tipo_avaliacao': request.form.get('tipo_avaliacao'),
            'peso': request.form.get('peso', nota.peso),
            'faltas': request.form.get('faltas', nota.faltas)
        }
        
        sucesso, resultado = nota_service.atualizar(id, dados)
        
        if sucesso:
            flash('Nota atualizada com sucesso!', 'success')
            return redirect(url_for('nota.listar_por_aluno', aluno_id=nota.aluno_id))
        else:
            flash(f'Erro ao atualizar nota: {resultado}', 'danger')

    return render_template('nota/editar.html', nota=nota)

@nota_bp.route('/notas/excluir/<int:id>')
@login_required
def excluir(id):
    nota = nota_service.buscar_por_id(id)
    if not nota:
        flash('Nota não encontrada.', 'danger')
        return redirect(url_for('nota.listar'))

    # Verifica se o usuário tem permissão para excluir a nota
    if not current_user.usuario == 'admin' and nota.professor_id != current_user.id:
        flash('Você não tem permissão para excluir esta nota.', 'danger')
        return redirect(url_for('nota.listar'))

    aluno_id = nota.aluno_id  # Guarda o ID do aluno antes de excluir
    sucesso, mensagem = nota_service.excluir(id)
    
    if sucesso:
        flash('Nota excluída com sucesso!', 'success')
    else:
        flash(f'Erro ao excluir nota: {mensagem}', 'danger')
    
    return redirect(url_for('nota.listar_por_aluno', aluno_id=aluno_id)) 