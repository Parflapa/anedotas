from flask import Flask, session, redirect, url_for   # classe usada para instanciar a aplicação web
import os


def criar_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SK', 'dev-inseguro')

    @app.context_processor
    def inject_user():
        return {
            "user_logado": session.get("user_id"),
            "username": session.get("username")
        }

    # importar e registar blueprints no fim
    from app.routes.rt_core import core
    from app.routes.rt_anedotas import anedotas
    from app.routes.rt_categorias import categorias
    from app.routes.rt_utilizadores import utilizadores
    from app.routes.rt_antenticacao import autenticacao

    app.register_blueprint(core)
    app.register_blueprint(anedotas)
    app.register_blueprint(categorias)
    app.register_blueprint(utilizadores)
    app.register_blueprint(autenticacao)

    return app
    