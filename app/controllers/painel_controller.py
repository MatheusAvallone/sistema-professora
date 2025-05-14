from flask import Blueprint, render_template
from flask_login import login_required, current_user

painel_bp = Blueprint('painel', __name__)

@painel_bp.route('/painel')
@login_required
def index():
    return render_template('painel/index.html', usuario=current_user)
