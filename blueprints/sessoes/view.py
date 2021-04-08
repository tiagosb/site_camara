from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask.helpers import flash
from blueprints.utils import requer_login
from blueprints.sessoes.controler import SessaoControler
from blueprints.forms import FormSessao

bp = Blueprint("sessao", __name__)
sessao_ctrl = SessaoControler()


@bp.route("/admin/sessoes")
@requer_login
def painel_sessoes():

    page = request.args.get("page", type=int, default=1) or 1
    sessoes = sessao_ctrl.listar_tudo(apenas_ativas=False, pagina=page)

    return render_template(
        "admin/painel-sessoes.html",
        sessoes=sessoes
    )


@bp.route("/sessao/<int:id>", methods=["get"])
def sessao(id):
    return render_template(
        "public/sessao.html", sessao_escolhida=sessao_ctrl.buscar_por_id(id)
    )


@bp.route("/sessoes")
def sessoes():
    page = request.args.get("page", type=int, default=1) or 1
    sessoes = sessao_ctrl.listar_tudo(pagina=page)

    return render_template("public/sessoes.html", sessoes=sessoes)


@bp.route("/sessao/atualizar-status", methods=["post"])
@requer_login
def atualizar_status():
    id = request.get_json().get("id")
    return sessao_ctrl.atualizar_status(id)


@bp.route("/admin/sessoes/nova", methods=["GET", "POST"])
@requer_login
def nova():
    form = FormSessao()
    if request.method == "POST":
        if form.validate_on_submit():
            if sessao_ctrl.cadastrar(
                form.tipo.data, form.data.data, form.hora.data, form.detalhes.data
            ):
                flash("Ok, nova sessão cadastrada.", "success")
                return redirect(url_for("sessao.painel_sessoes"))
            else:
                flash(
                    "Ops.. ocorreu um erro inesperado. A sesão não foi cadastrada. Por favor, verifique e tente novamente.",
                    "danger",
                )
        else:
            print(form.errors)
            flash(
                "Existem erros no formulário. Por favor, verifique e tente novamente.",
                "warning",
            )
    return render_template("admin/nova-sessao.html", form=form)


@bp.route("/admin/sessoes/editar/<int:id>", methods=["GET", "POST"])
@requer_login
def editar(id):
    form = FormSessao()
    sessao = sessao_ctrl.buscar_por_id(id)
    if request.method == "POST":
        if form.validate_on_submit():
            if sessao_ctrl.atualizar(
                id, form.tipo.data, form.data.data, form.hora.data, form.detalhes.data
            ):
                flash("Ok, sessão atualizada.", "success")
                return redirect(url_for("sessao.painel_sessoes"))
            else:
                flash("Ops.. não foi possível atualizar. Verifique e tente novamente.")
                return render_template("admin/editar-sessao.html", form=form)
    if request.method == "GET":
        if not sessao:
            flash(
                "Ops..não foi possível carregar os dados da sessão para editar. Verifique e tente novamente.",
                "danger",
            )
            return redirect(url_for("sessao.painel_sessoes"))
        form.process(obj=sessao)
        return render_template("admin/editar-sessao.html", form=form)
