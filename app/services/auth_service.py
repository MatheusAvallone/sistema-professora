from app.models.professor import Professor, db

class AuthService:
    def verificar_admin_existe(self):
        """Verifica se já existe um usuário admin no sistema"""
        return Professor.query.filter_by(usuario='admin').first() is not None

    def verificar_login(self, usuario, senha):
        professor = Professor.query.filter_by(usuario=usuario).first()
        print(f"Tentativa de login - Usuário: {usuario}")
        print(f"Professor encontrado: {professor is not None}")
        
        if professor and professor.check_senha(senha):
            print("Login bem-sucedido!")
            return True
        print("Login falhou - senha incorreta ou usuário não encontrado")
        return False

    def criar_admin_padrao(self):
        """Cria um usuário admin padrão se não existir"""
        try:
            # Verifica se já existe um admin
            admin = Professor.query.filter_by(usuario='admin').first()
            if not admin:
                print("Criando usuário admin...")
                admin = Professor(
                    usuario='admin',
                    nome='Administrador',
                    email='admin@sistema.com',
                    disciplina='Administração',
                    ativo=True
                )
                admin.set_senha('1234')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado com sucesso!")
                
                # Verifica se foi realmente criado
                admin_check = Professor.query.filter_by(usuario='admin').first()
                if admin_check:
                    print(f"✅ Admin verificado no banco: {admin_check.usuario}")
                    # Testa a senha
                    if admin_check.check_senha('1234'):
                        print("✅ Senha do admin verificada com sucesso!")
                    else:
                        print("❌ Erro na verificação da senha do admin!")
            else:
                print("⚠️ Usuário admin já existe!")
                # Atualiza os dados do admin existente
                admin.nome = 'Administrador'
                admin.email = 'admin@sistema.com'
                admin.disciplina = 'Administração'
                admin.ativo = True
                admin.set_senha('1234')
                db.session.commit()
                print("✅ Dados do admin atualizados!")
        except Exception as e:
            print(f"❌ Erro ao criar/atualizar admin: {str(e)}")
            db.session.rollback()

    def criar_professor(self, dados):
        """Cria um novo professor com senha hasheada"""
        try:
            if not Professor.query.filter_by(usuario=dados['usuario']).first():
                professor = Professor(
                    usuario=dados['usuario'],
                    nome=dados['nome'],
                    email=dados['email'],
                    telefone=dados['telefone'],
                    disciplina=dados['disciplina'],
                    ativo=True
                )
                professor.set_senha(dados['senha'])
                db.session.add(professor)
                db.session.commit()
                print(f"✅ Professor {dados['usuario']} criado com sucesso!")
                return True
            print(f"⚠️ Professor {dados['usuario']} já existe!")
            return False
        except Exception as e:
            print(f"❌ Erro ao criar professor: {str(e)}")
            db.session.rollback()
            return False

    def alterar_senha(self, usuario, senha_atual, nova_senha):
        """Altera a senha de um professor"""
        try:
            professor = Professor.query.filter_by(usuario=usuario).first()
            if professor and professor.check_senha(senha_atual):
                professor.set_senha(nova_senha)
                db.session.commit()
                print(f"✅ Senha alterada com sucesso para {usuario}")
                return True
            print(f"❌ Falha ao alterar senha para {usuario}")
            return False
        except Exception as e:
            print(f"❌ Erro ao alterar senha: {str(e)}")
            db.session.rollback()
            return False
