from flask import session, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
import functools
import os
from werkzeug.utils import secure_filename
from dynaconf import settings


def requer_login(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "auth" not in session or not session["auth"]:
            flash("Informe seu usuário e senha.", category="warning")
            return redirect(url_for("usuario.login"))
        return func(*args, **kwargs)

    return secure_function


def upload_doc(arquivo):
    nome = secure_filename(arquivo.filename).lower()
    if nome != "":
        extensao = os.path.splitext(nome)[1]
        if extensao in [".doc", ".docx", ".odt", ".odf", ".pdf", ".rtf", ".txt"]:
            caminho = os.path.join(settings["UPLOAD_FOLDER_DOC"], nome)
            arquivo.save(caminho)
            return nome
    return None


def upload_image(arquivo):
    nome = secure_filename(arquivo.filename).lower()
    if nome != "":
        extensao = os.path.splitext(nome)[1]
        if extensao in [".png", ".jpg", ".jpeg", ".gif"]:
            caminho = os.path.join(settings["UPLOAD_FOLDER_IMG"], nome)
            arquivo.save(caminho)
            return nome
    return None
