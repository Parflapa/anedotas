from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.services.serv_anedotas import detalhes_da_anedota, dash_board_categorias_anedotas, adicionar_anedota, editar_anedota, eliminar_anedota
from app.services.serv_categorias import listar_categorias
from app.utils.auth import login_required


anedotas = Blueprint('anedotas', __name__, url_prefix="/anedotas")


@anedotas.route("/")
def dashboard():
    dados = dash_board_categorias_anedotas()
    return render_template("home.html", anedotas_por_categoria=dados)


@anedotas.route("/<int:anedota_id>")
def detalhes_anedota(anedota_id):
    detalhes = detalhes_da_anedota(anedota_id)
    return render_template("detalhes_da_anedota.html", detalhes=detalhes)


@anedotas.route("/adicionar", methods=["GET", "POST"])
@login_required
def adicionar():
    if request.method == "POST":
        texto       = request.form.get("ftexto")
        categoria   = request.form.get("fcategoria")
        utilizador  = session.get("id_utilizador")

        # validação básica
        if not texto or not categoria:
            flash("Preenche todos os campos.", "error")
            return redirect(url_for("anedotas.adicionar"))

        sucesso = adicionar_anedota(utilizador, texto, categoria)

        if sucesso:
            flash("Anedota criada com sucesso!", "success")
            return redirect(url_for("utilizadores.area_pessoal"))
        else:
            flash("Erro ao criar anedota.", "error")
        

    categorias  = listar_categorias()
    return render_template("adicionar.html", categorias=categorias)


@anedotas.route("/editar/<int:anedota_id>", methods=["GET", "POST"])
@login_required
def editar(anedota_id):
    if request.method == "POST":
        texto       = request.form.get("ftexto")
        categoria   = request.form.get("fcategoria")
        
        # validação básica
        if not texto or not categoria:
            flash("Preenche todos os campos.", "error")
            return redirect(url_for("anedotas.editar"))
        
        sucesso = editar_anedota(anedota_id,texto,categoria)

        if sucesso:
            flash("Anedota editada com sucesso!", "success")
            return redirect(url_for("utilizadores.area_pessoal"))
        else:
            flash("Erro ao editar anedota.", "error")


    dados = {
        "anedota"       : detalhes_da_anedota(anedota_id),
        "categorias"    : listar_categorias()
    }
    return render_template("editar.html", dados=dados)


@anedotas.route("/eliminar/<int:anedota_id>", methods=["POST"])
@login_required
def eliminar(anedota_id):

    sucesso = eliminar_anedota(anedota_id)

    if sucesso:
        flash("Anedota eliminada com sucesso!", "success")
    else:
        flash("Erro ao eliminar anedota.", "error")

    return redirect(url_for("utilizadores.area_pessoal"))