from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.services.serv_utilizadores import listar_utilizadores, listar_todas_anedotas_deste_utilizador, registar_utilizador  # type:ignore
from app.services.serv_paises import listar_paises
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



@utilizadores.route("/registo", methods=["GET","POST"])
def registo():
    if request.method == "POST":
        nome        = request.form.get("fnome")
        nick        = request.form.get("fnick")
        email       = request.form.get("femail")
        pais        = request.form.get("fpais")
        password    = request.form.get("fpass1")

        sucesso = registar_utilizador(nome, email, nick, pais, password)

        if sucesso:
            flash("Utilizador registado com sucesso!", "success")
            return redirect(url_for("anedotas.dashboard"))
        else:
            flash("Erro ao registar utilizador. ", "error")
    
    paises = listar_paises()
    return render_template("registo.html", paises=paises)