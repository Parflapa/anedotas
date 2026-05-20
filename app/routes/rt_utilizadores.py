from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from app.services.serv_utilizadores import listar_utilizadores, listar_todas_anedotas_deste_utilizador, registar_utilizador, confirmar_registo, verificar_se_email_ja_esta_registado  # type:ignore
from app.services.serv_paises import listar_paises
from app.utils.auth import login_required
from itsdangerous import URLSafeTimedSerializer


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
        nome     = request.form.get("fnome")
        nick     = request.form.get("fnick")
        email    = request.form.get("femail")
        pais     = request.form.get("fpais")
        password = request.form.get("fpass1")
        # debug: flash(f"{nome}, {nick}, {email}, {pais}, {password}.", "success")
        # output: Testolino, Testas, lapa.pedro@gmail.com, 1, batatas. 
        # debug: return redirect(url_for("anedotas.dashboard"))
        email_ja_existe = verificar_se_email_ja_esta_registado(email)
        if email_ja_existe:
            flash(f"O email '{email}' já está registado.", "error")
            return redirect(url_for("anedotas.dashboard"))

        sucesso = registar_utilizador(nome, email, nick, pais, password)
        if sucesso:
            flash("Para concluir o seu registo foi-lhe enviado um email de confirmação.", "success")
        else:
            flash("Erro no registo do utilizador.", "error")
        return redirect(url_for("anedotas.dashboard"))

    paises = listar_paises()
    return render_template("registo.html", paises=paises)



@utilizadores.route("/confirmacao/<token>",methods=["GET"])
def confirmacao(token):

    link_recebido = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        dados = link_recebido.loads(
            token,
            salt='confirmar-email',
            max_age= 24 * 60 * 60  # aqui confirmo a validade que desejo: 24 horas
        )
    except Exception:
        flash("Token inválido ou expirado", "error")
        return redirect(url_for("anedotas.dashboard"))

    email_recebido = dados['email']
    
    sucesso = confirmar_registo(email_recebido)

    if sucesso:
        flash(f"O seu email '{email_recebido}' foi confirmado e seu registo está concluído.")
    else:
        flash(f"O seu email '{email_recebido}' foi confirmado mas o registo não pode ser concluído. Por favor tente novamente.")

    return redirect(url_for("anedotas.dashboard"))



    if sucesso:
        flash("Utilizador registado com sucesso!", "success")
        return redirect(url_for("anedotas.dashboard"))
    else:
        flash("Erro ao registar utilizador. Por favor tente novamente", "error")
        return redirect(url_for("anedotas.dashboard"))

