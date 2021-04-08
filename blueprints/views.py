from flask import Blueprint
from flask import render_template
from flask import send_from_directory
from .utils import requer_login
from dynaconf import settings
from .noticias.controler import NoticiasControler
from .vereadores.controler import VereadorControler
from .sessoes.controler import SessaoControler
from .documentos.controler import DocumentoControler


bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    noticias_ctrl = NoticiasControler()
    vereadores_ctrl = VereadorControler()
    sessoes_ctrl = SessaoControler()

    sessao = sessoes_ctrl.proxima_sessao()

    return render_template(
        "public/index.html",
        noticias=noticias_ctrl.listar_tudo(apenas_destacadas=True),
        vereadores=vereadores_ctrl.listar_todos_sem_paginacao(),
        sessao=sessao
    )


@bp.route("/admin")
@requer_login
def admin():
    return render_template("admin/painel-administrativo.html")


@bp.route("/media/img/<filename>")
def media_img(filename):
    return send_from_directory(settings.get("UPLOAD_FOLDER_IMG"), filename)


@bp.route("/media/doc/<filename>")
def media_doc(filename):
    return send_from_directory(settings.get("UPLOAD_FOLDER_DOC"), filename)


@bp.app_errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("public/pagina-nao-encontrada.html"), 404


def init_app(app):
    app.register_blueprint(bp)
