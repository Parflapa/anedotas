from flask import Flask, session   # classe usada para instanciar a aplicação web
import os
from dotenv import load_dotenv
load_dotenv("/var/www/vhosts/websis.pt/credenciais/crd_anedotas")


def criar_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SK', 'dev-inseguro')

    # context_processor é uma função de injeção de variáveis para templates Jinja.
    # é executado APENAS quando um template é renderizado
    @app.context_processor
    def inject_user():
        return {
            "user_logado": session.get("user_id"),
            "username": session.get("username")
        }

    # importar e registar blueprints no fim
    from app.routes.rt_anedotas import anedotas
    from app.routes.rt_categorias import categorias
    from app.routes.rt_utilizadores import utilizadores
    from app.routes.rt_antenticacao import autenticacao

    app.register_blueprint(anedotas)
    app.register_blueprint(categorias)
    app.register_blueprint(utilizadores)
    app.register_blueprint(autenticacao)

    return app
    