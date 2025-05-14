import bcrypt
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Professor.query.get(int(user_id))

class Professor(db.Model, UserMixin):
    __tablename__ = 'professoras'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255))
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    disciplina = db.Column(db.String(50))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    def set_senha(self, senha):
        try:
            # Converte a senha para bytes se for string
            if isinstance(senha, str):
                senha = senha.encode('utf-8')
            # Gera o salt e faz o hash da senha
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha, salt)
            # Armazena o hash como string
            self.senha_hash = senha_hash.decode('utf-8')
            print(f"✅ Hash da senha gerado com sucesso para {self.usuario}")
        except Exception as e:
            print(f"❌ Erro ao gerar hash da senha: {str(e)}")
            raise

    def check_senha(self, senha):
        try:
            print(f"Verificando senha para {self.usuario}")
            # Converte a senha e o hash para bytes
            if isinstance(senha, str):
                senha = senha.encode('utf-8')
            if self.senha_hash:
                senha_hash = self.senha_hash.encode('utf-8')
                # Verifica se a senha corresponde ao hash
                resultado = bcrypt.checkpw(senha, senha_hash)
                print(f"Resultado da verificação: {'✅ Senha correta' if resultado else '❌ Senha incorreta'}")
                return resultado
            print("❌ Hash da senha não encontrado")
            return False
        except Exception as e:
            print(f"❌ Erro ao verificar senha: {str(e)}")
            return False

    def to_dict(self):
        """Converte o objeto em um dicionário para serialização."""
        return {
            'id': self.id,
            'usuario': self.usuario,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'disciplina': self.disciplina,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo
        }

    def __repr__(self):
        return f'<Professor {self.nome} ({self.usuario})>' 