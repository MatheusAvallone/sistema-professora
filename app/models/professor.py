import bcrypt
from app import db

class Professor(db.Model):
    __tablename__ = 'professoras'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255))  # Aumentado para acomodar o hash bcrypt

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

    def __repr__(self):
        return f'<Professor {self.usuario}>' 