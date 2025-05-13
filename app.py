from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os


app = Flask(__name__)
app.secret_key = "chave_super_secreta" # Mude para algo seguro em produção
DATABASE = "database.db"


# --- Conexão com o banco ---

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Criar Tabelas no primeiro uso ---

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professoras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')

        # Criar um usuário padrão (usuario: admin, senha: 1234)

        cursor.execute("SELECT * FROM professoras WHERE usuario = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO professoras (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
        db.commit()

# --- Rota de Login ---

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM professoras WHERE usuario=? AND senha=?", (usuario, senha))
        prof = cursor.fetchone()
        if prof:
            session["logado"] = True
            session["usuario"] = usuario
            return redirect(url_for("painel"))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos.")
    return render_template("login.html")


# --- Painel Principal ---

@app.route("/painel")
def painel():
    if not session.get("logado"):
        return redirect(url_for("login"))
    return render_template("painel.html", usuario=session.get("usuario"))


# --- Logout ---

@app.route("/logout")
def logout():
    session.pop("logado", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
