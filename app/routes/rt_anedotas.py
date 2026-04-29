from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.services.serv_anedotas import detalhes_da_anedota, dash_board_categorias_anedotas, adicionar_anedota
from app.services.serv_categorias import listar_categorias
from app.utils.auth import login_required


anedotas = Blueprint('anedotas', __name__)


@anedotas.route("/")
def dashboard():
    dados = dash_board_categorias_anedotas()
    return render_template("home.html", anedotas_por_categoria=dados)


@anedotas.route("/anedota/<int:anedota_id>")
def detalhes_anedota(anedota_id):
    detalhes = detalhes_da_anedota(anedota_id)
    return render_template("detalhes_da_anedota.html", detalhes=detalhes)


@anedotas.route("/adicionar", methods=["GET", "POST"])
@login_required
def adicionar():
    if request.method == "POST":
        texto       = request.form.get("ftexto"),
        categoria   = request.form.get("fcategoria")
        utilizador  = session.get("id_utilizador")

        # validação básica
        if not texto or not categoria:
            flash("Preenche todos os campos.", "error")
            return redirect(url_for("anedotas.adicionar"))

        sucesso = adicionar_anedota(utilizador, texto, categoria)

        if sucesso:
            flash("Anedota criada com sucesso!", "success")
            return redirect(url_for("anedotas.dashboard"))
        else:
            flash("Erro ao criar anedota.", "error")
        

    categorias  = listar_categorias()
    return render_template("adicionar.html", categorias=categorias)


@anedotas.route("/editar/<int:anedota_id>")
@login_required
def editar(anedota_id):
    categorias = listar_categorias()
    return render_template("editar.html", categorias=categorias)


@anedotas.route("/eliminar/<int:anedota_id>")
@login_required
def eliminar(anedota_id):
    return render_template("eliminar.html")