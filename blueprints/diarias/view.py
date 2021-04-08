from decimal import Decimal
from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from blueprints.diarias.controler import DiariaControler
from blueprints.utils import requer_login
from datetime import datetime
from blueprints.forms import FormDiaria

bp = Blueprint("diaria", __name__)
diaria_ctrl = DiariaControler()


@bp.route("/admin/diarias")
@requer_login
def painel_diarias():
    pagina = request.args.get("page") or 1
    diarias = diaria_ctrl.listar_tudo(pagina=pagina)

    return render_template("admin/painel-diarias.html", diarias=diarias)


@bp.route("/admin/diarias/nova", methods=["GET", "POST"])
@requer_login
def nova():
    form = FormDiaria()
    if request.method == "POST":
        if form.validate_on_submit():
            if diaria_ctrl.cadastrar(
                form.nome.data,
                form.data.data,
                form.destino.data,
                form.motivo.data,
                str(form.valor.data),
            ):
                flash("Ok, nova diária cadastrada.", "success")
                return redirect(url_for("diaria.painel_diarias"))
            # Erro interno -> verificar
            flash(
                "Ops.. ocorreu um erro, inesperado. Por favor, tente novamente.",
                "danger",
            )
        else:
            flash(
                "Foram encontrados erros no formulário, por favor verifique e tente novamente.",
                "warning",
            )
        return render_template("admin/nova-diaria.html", form=form)

    if request.method == "GET":
        return render_template("admin/nova-diaria.html", form=form)


@bp.route("/admin/diarias/editar/<int:id>", methods=["GET", "POST"])
@requer_login
def editar(id):

    form = FormDiaria()
    diaria = diaria_ctrl.consultar_por_id(id)

    if request.method == "POST":
        if form.validate_on_submit():
            if diaria_ctrl.atualizar(
                form.id.data,
                form.nome.data,
                form.data.data,
                form.destino.data,
                form.motivo.data,
                str(form.valor.data),
            ):
                flash("Ok, a diária foi atualizada.", "success")
                return redirect(url_for("diaria.painel_diarias"))
            else:
                flash(
                    "Ops.. ocorreu um erro inesperado. Por favor, tente novamente.",
                    "danger",
                )
        else:
            flash(
                "Existem erros no formulário. Por favor, verifique e tente novamente.",
                "warning",
            )
        return render_template("admin/editar-diaria.html", form=form)

    if request.method == "GET":
        form.process(obj=diaria)
        form.valor.data = Decimal(diaria.valor)
        return render_template("admin/editar-diaria.html", form=form)


@bp.route("/diaria/<int:id>")
def diaria(id):
    return render_template(
        "public/diaria.html", diaria=diaria_ctrl.consultar_por_id(id)
    )


@bp.route("/diarias")
def diarias():
    pagina = request.args.get("page") or 1
    diarias = diaria_ctrl.listar_tudo(pagina=pagina)

    return render_template("public/diarias.html", diarias=diarias)
