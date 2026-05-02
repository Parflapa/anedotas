from flask import Blueprint, render_template
from app.services.serv_categorias import listar_categorias, listar_todas_anedotas_desta_categoria


categorias = Blueprint('categorias', __name__, url_prefix="/categorias")


@categorias.route("/")
def lista_categorias():
    return render_template("lista_categorias.html", lista_categorias = listar_categorias())


@categorias.route("/<int:categoria_id>")
def detalhes_categoria(categoria_id):
    detalhes = listar_todas_anedotas_desta_categoria(categoria_id)
    return render_template("detalhes_da_categoria.html", detalhes = detalhes)



