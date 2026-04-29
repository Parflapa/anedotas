from flask import Blueprint, request, session, redirect, url_for, flash
from app.services.serv_utilizadores import validar_login


autenticacao = Blueprint("autenticacao", __name__) 


@autenticacao.route("/login", methods=["POST"])
def login():
    nick_ou_email   = request.form.get("user")
    password        = request.form.get("password")
    resultado       = validar_login(nick_ou_email, password)
    if resultado["sucesso"]:
        user                        = resultado["utilizador"]
        session["id_utilizador"]    = user["id"]
        session["nome_utilizador"]  = user["nome"]
        session["nick_utilizador"]  = user["nick"]
        session["email_utilizador"] = user["email"]
        flash("Login efetuado com sucesso.", "success")
    else:
        flash(resultado["mensagem"], "error")
    return redirect(url_for("anedotas.dashboard"))


@autenticacao.route("/logout")
def logout():
    session.clear()
    flash("Sessão terminada.", "success")
    return redirect(url_for("anedotas.dashboard"))


