from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect, flash
from blueprints.utils import requer_login, upload_image
from blueprints.vereadores.controler import VereadorControler
from blueprints.forms import FormVereador

bp = Blueprint("vereador", __name__)
vereador_ctrl = VereadorControler()


@bp.route("/admin/vereadores")
@requer_login
def painel_vereadores():

    page = request.args.get("page") or 1
    vereadores = vereador_ctrl.listar_todos(pagina=page, apenas_ativos=False)

    return render_template(
        "admin/painel-vereadores.html", vereadores=vereadores, page=page
    )


@bp.route("/admin/vereadores/novo", methods=["GET", "POST"])
@requer_login
def novo():
    form = FormVereador()
    if request.method == "GET":
        return render_template("admin/novo-vereador.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            foto = form.thumb.data
            if foto:
                foto = upload_image(foto)
                if not foto:
                    flash(
                        "O upload da fotografia falhou. Por favor, verifique e tente novamente.",
                        category="danger",
                    )
                    return render_template("admin/novo-vereador.html", form=form)
            if vereador_ctrl.cadastrar(
                form.nascimento.data,
                form.nome_civil.data,
                form.nome_urna.data,
                form.naturalidade.data,
                form.uf.data,
                form.ocupacao.data,
                form.escolaridade.data,
                form.partido.data,
                form.legislaturas.data,
                form.telefone.data,
                form.email.data,
                form.detalhes.data,
                foto,
            ):
                flash("Ok, novo vereador cadastrado.", category="success")
                return redirect(url_for("vereador.painel_vereadores"))
            else:
                flash(
                    "Ocorreu um erro inesperado, o verador não foi cadastrado. Por favor, verifique os dados e tente outra vez.",
                    category="danger",
                )
        else:
            flash(
                "Foram encontrados erros no formulário. Verifique e tente de novo.",
                category="warning",
            )
        return render_template("admin/novo-vereador.html", form=form)


@bp.route("/vereadores")
def vereadores():
    pagina = request.args.get("page") or 1
    vereadores = vereador_ctrl.listar_todos(pagina=pagina)

    return render_template(
        "public/vereadores.html",
        vereadores=vereadores,
        pagina=pagina,
    )


@bp.route("/vereador/<int:id>")
def vereador(id):
    return render_template(
        "public/vereador.html", vereador=vereador_ctrl.buscar_por_id(id)
    )


@bp.route("/atualizar-status", methods=["post"])
@requer_login
def atualizar_status():
    id = request.get_json().get("id")
    return vereador_ctrl.atualizar_status(id)


@bp.route("/admin/vereadores/editar/<int:id>", methods=["POST", "GET"])
@requer_login
def editar(id):
    form = FormVereador()
    vereador = vereador_ctrl.buscar_por_id(id)

    if request.method == "POST":
        if form.validate_on_submit():
            nova_foto = None
            if form.thumb.data:
                nova_foto = upload_image(form.thumb.data)
                if not nova_foto:
                    flash(
                        "Ops.. houve um erro no upload da foto. Por favor, verifique e tente outra vez.",
                        category="danger",
                    )
                    return render_template("admin/editar-vereador.html", form=form)
            if vereador_ctrl.atualizar(
                form.id.data,
                form.nascimento.data,
                form.nome_civil.data,
                form.nome_urna.data,
                form.naturalidade.data,
                form.uf.data,
                form.ocupacao.data,
                form.escolaridade.data,
                form.partido.data,
                form.legislaturas.data,
                form.telefone.data,
                form.email.data,
                form.detalhes.data,
                nova_foto,
            ):
                flash("Ok, os dados foram atualizados.", category="success")
                return redirect(url_for("vereador.painel_vereadores"))
            else:
                flash(
                    "Ops.. ocorreu um erro inesperado, as alterações não foram salvas. Verifique e tente novamente.",
                    category="danger",
                )
        else:
            flash(
                "Foram encontrados erros no preenchimento do formulário. Verifique e tente novamente.",
                category="warning",
            )
        return render_template("admin/editar-vereador.html", form=form)

    if request.method == "GET":
        form.process(obj=vereador)
        if vereador.foto:
            form.thumb.data = url_for("views.media_img", filename=vereador.foto)
            print(form.thumb.data)
        return render_template("admin/editar-vereador.html", form=form)
