from flask import Flask, session   # classe usada para instanciar a aplicação web
from datetime import datetime
import os
import sys
import logging
from dotenv import load_dotenv
from app.utils.extensoes import mail
from werkzeug.middleware.proxy_fix import ProxyFix


caminho_local = r"C:\xampp\credenciais"
caminho_prod = "/var/www/vhosts/websis.pt/credenciais/"
ficheiro_env = "crd_anedotas.env"

if os.path.exists(r"C:\xampp\credenciais\crd_anedotas.env"):
    load_dotenv(os.path.join(caminho_local, ficheiro_env))
else:
    load_dotenv(os.path.join(caminho_prod, ficheiro_env))



def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # evita duplicação real (não só "existência")
    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # opcional: evita propagação duplicada
    logger.propagate = False




def criar_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SK', 'dev-inseguro')
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1
    )

    # mail config
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')              # type:ignore
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
    mail.init_app(app)

    # print("MAIL_USERNAME:", os.environ.get('MAIL_USERNAME'))
    # print("MAIL_PORT:", os.environ.get('MAIL_PORT'))
    # print("MAIL_SERVER:", os.environ.get('MAIL_SERVER'))
    # print("MAIL_PASSWORD:", os.environ.get('MAIL_PASSWORD'))
    # print("MAIL_USE_SSL:", os.environ.get('MAIL_USE_SSL'))

    setup_logging()

    # context_processor é uma função de injeção de variáveis para templates Jinja.
    # é executado APENAS quando um template é renderizado
    @app.context_processor
    def inject_vars():
        return {
            "user_logado"   : session.get("id_utilizador"),
            "username"      : session.get("nome_utilizador"),
            "data_atual"    : datetime.now()
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
    