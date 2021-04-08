from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound
from ext.database import Usuario, con
from .forms import FormLogin
import bcrypt

bp = Blueprint("usuario", __name__)


@bp.route("/usuarios/cadastrar", methods=["post"])
def cadastrar():
    try:
        user = request.form["usuario"]
        senha = bcrypt.hashpw(request.form["senha"].encode(), bcrypt.gensalt())
        novo_usuario = Usuario(user, senha)
        con.session.add(novo_usuario)
        con.session.commit()
        return jsonify({"sucesso": True, "id": novo_usuario.id})
    except Exception as erro:
        print(erro)
        return jsonify({"sucesso": False})


@bp.route("/login", methods=["get", "post"])
def login():
    
    # Salvar informações de acesso em log ou na base de dados
    sistema_operacional = request.user_agent.platform
    navegador = request.user_agent.browser
    ip = request.remote_addr
    print(f"Acessado a partir do navegador {navegador} no sistema operacional {sistema_operacional} com ip {ip}")
    
    form = FormLogin()
    if request.method == "POST":
        if form.validate_on_submit():
            user = form.usuario.data
            try:
                user_auth = (
                    con.session.query(Usuario).filter(Usuario.usuario == user).one()
                )

                if bcrypt.checkpw(form.senha.data.encode(), user_auth.senha):
                    flash("Bem vindo!", category="success")
                    session["auth"] = True
                    return redirect(url_for("views.admin"))
                else:
                    flash("Senha incorreta.", category="warning")
            except NoResultFound:
                flash("Usuário inexistente.", category="warning")
        else:
            print(form.errors)
    return render_template("public/login.html", form=form, mensagem=None)


@bp.route("/logout")
def logout():
    msg = "Você não está conectado."

    if "auth" in session:
        session.pop("auth", None)
        msg = "Você foi desconectado."

    flash(msg, category="warning")
    return redirect(url_for("usuario.login"))
