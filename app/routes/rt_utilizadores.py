from flask import Blueprint, render_template, session, redirect, url_for
from app.services.serv_utilizadores import listar_utilizadores, listar_todas_anedotas_deste_utilizador  # type:ignore
from app.utils.auth import login_required


utilizadores = Blueprint('utilizadores', __name__, url_prefix="/utilizadores")


@utilizadores.route("/")
def lista_utilizadores():
    return render_template("lista_utilizadores.html", lista_utilizadores = listar_utilizadores())


@utilizadores.route("/<int:utilizador_id>")
def detalhes_utilizador(utilizador_id):
    detalhes = listar_todas_anedotas_deste_utilizador(utilizador_id)
    return render_template("detalhes_do_utilizador.html", detalhes = detalhes)


@utilizadores.route("/area_pessoal")
@login_required
def area_pessoal():
    id_utilizador = session.get("id_utilizador")

    if not id_utilizador:
        return redirect(url_for("utilizadores.login"))

    detalhes = listar_todas_anedotas_deste_utilizador(id_utilizador)
    return render_template("area_pessoal.html", detalhes = detalhes)