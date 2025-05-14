from flask import Blueprint, render_template, request, redirect, session, url_for
from app.services.auth_service import AuthService
from app.models.professor import Professor

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, redireciona para o painel
    if session.get("logado"):
        return redirect(url_for('painel.index'))

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        
        if auth_service.verificar_login(usuario, senha):
            session["logado"] = True
            session["usuario"] = usuario
            print("✅ Login bem-sucedido, redirecionando para o painel...")
            return redirect(url_for('painel.index'))
        else:
            return render_template("auth/login.html", erro="Usuário ou senha inválidos.")
    
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
