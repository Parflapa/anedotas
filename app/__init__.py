from flask import Flask, session, redirect   # classe usada para instanciar a aplicação web
import os


def criar_app():
    app = Flask(__name__)
    
    # config básica
    app.config['SECRET_KEY'] = os.environ.get('SK', 'dev-inseguro')

    # CONTEXT PROCESSOR AQUI
    @app.context_processor
    def inject_user():
        return {
            "user_logado": session.get("user_id"),
            "username": session.get("username")
        }

    # Necessário para utilização de prefix 
    # rota de arranque (AQUI dentro, mas usando app)
    @app.route("/")
    def index():
        return redirect("/anedotas/")


    # registar blueprints
    from app.routes.rt_anedotas import anedotas
    app.register_blueprint(anedotas)
    
    from app.routes.rt_categorias import categorias
    app.register_blueprint(categorias)
    
    from app.routes.rt_utilizadores import utilizadores
    app.register_blueprint(utilizadores)
    
    from app.routes.rt_antenticacao import autenticacao
    app.register_blueprint(autenticacao)

    return app
    