from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.services.serv_categorias import listar_categorias, listar_todas_anedotas_desta_categoria, adicionar_categoria, editar_categoria, eliminar_categoria, dados_da_categoria
from app.utils.auth import login_required


categorias = Blueprint('categorias', __name__, url_prefix="/categorias")


@categorias.route("/")
def lista_categorias():
    return render_template("lista_categorias.html", lista_categorias = listar_categorias())


@categorias.route("/<int:categoria_id>")
def detalhes_categoria(categoria_id):
    detalhes = listar_todas_anedotas_desta_categoria(categoria_id)
    return render_template("detalhes_da_categoria.html", detalhes = detalhes)


@categorias.route("/area_categorias",methods=["POST","GET"])
@login_required
def area_categorias():
    id_utilizador = session.get("id_utilizador")

    if not id_utilizador:
        return redirect(url_for("utilizadores.login"))

    return render_template("area_categorias.html", lista_categorias = listar_categorias())


@categorias.route("/adicionar", methods=["GET","POST"])
@login_required
def adicionar():
    if request.method == "POST":
        nome   = request.form.get("fnome")

        # validação básica
        if not nome:
            flash("Preenche todos os campos.", "error")
            return redirect(url_for("categorias.adicionar"))

        sucesso = adicionar_categoria(nome)

        if sucesso:
            flash("Categoria criada com sucesso!", "success")
            return redirect(url_for("categorias.area_categorias"))
        else:
            flash("Erro ao criar categoria.", "error")
        
    return render_template("adicionar_categoria.html")


@categorias.route("/editar/<int:categoria_id>", methods=["GET", "POST"])
@login_required
def editar(categoria_id):
    if request.method == "POST":
        nome       = request.form.get("fnome")
        
        # validação básica
        if not nome:
            flash("Preenche todos os campos.", "error")
            return redirect(url_for("categorias.editar"))
        
        sucesso = editar_categoria(categoria_id,nome)

        if sucesso:
            flash("Categoria editada com sucesso!", "success")
            return redirect(url_for("categorias.area_categorias"))
        else:
            flash("Erro ao editar categoria.", "error")


    dados =  dados_da_categoria(categoria_id)
    return render_template("editar_categoria.html", dados=dados)


@categorias.route("/eliminar/<int:categoria_id>", methods=["POST"])
@login_required
def eliminar(categoria_id):
    sucesso = eliminar_categoria(categoria_id)
    if sucesso:
        flash("Categoria eliminada com sucesso!", "success")
    else:
        flash("Erro ao eliminar categoria.", "error")

    return redirect(url_for("categorias.area_categorias"))