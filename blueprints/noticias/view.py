from flask import Blueprint, render_template, request, url_for, redirect, abort, flash
import flask
from blueprints.utils import requer_login, upload_image
from blueprints.forms import FormNoticia
from blueprints.noticias.controler import NoticiasControler

bp = Blueprint("noticia", __name__)

noticias_ctrl = NoticiasControler()


@bp.route("/noticias/<int:id>")
def noticia(id):
    post = noticias_ctrl.buscar_por_id(id) or abort(404)
    return render_template("public/noticia.html", post=post)


@bp.route("/noticias")
def noticias():

    page = request.args.get("page", type=int, default=1) or 1
    noticias = noticias_ctrl.listar_tudo(apenas_ativas=True, pagina=page)
    return render_template("public/noticias.html", noticias=noticias)


@bp.route("/admin/noticias")
@requer_login
def painel_noticias():
    page = request.args.get("page", type=int, default=1) or 1
    noticias = noticias_ctrl.listar_tudo(apenas_ativas=False, pagina=page)

    return render_template(
        "admin/painel-noticias.html",
        noticias=noticias,
    )


@bp.route("/admin/noticias/nova", methods=["get", "post"])
@requer_login
def nova():
    form = FormNoticia()
    if request.method == "POST":
        if form.validate_on_submit():

            destaque = False
            if form.destaque.data == "sim":
                destaque = True

            thumb_url = None
            if form.thumb.data:
                thumb_url = upload_image(form.thumb.data)

            if noticias_ctrl.cadastrar(
                form.titulo.data,
                form.conteudo.data,
                thumb_url,
                form.categoria.data,
                destaque,
            ):
                flash("Ok! A noticia foi cadastrada.", category="success")
                return redirect(url_for("noticia.painel_noticias"))
            else:
                flash(
                    "Ops.. Ocorreu um erro, a noticia não foi cadastrada. Verifique os dados e tente novamente."
                )
        else:
            print(form.errors)
            flash("Preencha corretamente os campos obrigatórios.", category="warning")

    return render_template("admin/nova-noticia.html", form=form)


@bp.route("/admin/noticias/editar/<int:id>", methods=["get", "post"])
@requer_login
def editar(id):
    form = FormNoticia()
    noticia = noticias_ctrl.buscar_por_id(id)
    if request.method == "GET":
        if noticia:
            form.process(obj=noticia)
        else:
            flash(
                "Ops.. não foi possível carregar os dados da noticia para edição. Verifique e tente novamente.",
                category="danger",
            )
            return redirect(url_for("noticia.painel_noticias"))
    if request.method == "POST":
        if form.validate_on_submit():

            destaque = False
            if form.destaque.data == "sim":
                destaque = True

            nova_thumb = None
            if form.thumb.data:
                nova_thumb = upload_image(form.thumb.data)
                if not nova_thumb:
                    flash(
                        "Ops.. ocorreu um erro ao atualizar a imagem de capa. Por favor verifique e tente novamente.",
                        category="danger",
                    )
                    form.thumb.data = noticia.thumb
                    return render_template("admin/editar-noticia.html", form=form)

            if noticias_ctrl.atualizar(
                form.id.data,
                form.titulo.data,
                form.conteudo.data,
                nova_thumb,
                form.categoria.data,
                destaque,
            ):
                flash("Ok, a noticia foi atualizada.", category="success")
                return redirect(url_for("noticia.painel_noticias"))
            else:
                flash(
                    "Ops.. ocorreu um erro inesperado. As atualizações não foram salvas. Por favor, verifique os dados e tente novamente.",
                    category="danger",
                )
        else:
            if not form.thumb.data:
                form.thumb.data = noticia.thumb
            flash(
                "Foram encontrados erros no formulário. Por favor, verifique e tente de novo.",
                category="warning",
            )
            print(form.errors)
    return render_template("admin/editar-noticia.html", form=form)


@bp.route("/admin/noticias/alterar-status", methods=["post"])
@requer_login
def atualizar_status():
    id = request.get_json().get("id")
    return noticias_ctrl.atualizar_status(id)
