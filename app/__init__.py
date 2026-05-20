from flask import Flask, session   # classe usada para instanciar a aplicação web
import os
from dotenv import load_dotenv
from app.utils.extensoes import mail
load_dotenv("/var/www/vhosts/websis.pt/credenciais/crd_anedotas")


def criar_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SK', 'dev-inseguro')


    # mail config
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

    mail.init_app(app)


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
    