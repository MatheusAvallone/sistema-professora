from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps

painel_bp = Blueprint('painel', __name__, url_prefix='/painel')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logado"):
            print("❌ Usuário não está logado, redirecionando para login...")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@painel_bp.route('/')
@login_required
def index():
    print("✅ Renderizando página do painel...")
    return render_template('painel/index.html', usuario=session.get('usuario'))
