from functools import wraps
from flask import Blueprint, session, redirect, url_for, flash

autenticacao = Blueprint("autenticacao", __name__) 

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "id_utilizador" not in session:
            flash("A página que tentou aceder é protegida.", "error")
            return redirect(url_for("anedotas.dashboard"))  # homepage
        return view(*args, **kwargs)
    return wrapped_view
