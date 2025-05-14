from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import AuthService
from app.models.professor import Professor

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        
        professor = Professor.query.filter_by(usuario=usuario).first()
        
        if professor and professor.check_senha(senha):
            login_user(professor)
            print("✅ Login bem-sucedido, redirecionando para o painel...")
            return redirect(url_for('painel.index'))
        else:
            flash("Usuário ou senha inválidos.", "danger")
            return render_template("auth/login.html")
    
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado com sucesso.", "info")
    return redirect(url_for('auth.login'))
