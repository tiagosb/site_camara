from flask import Blueprint, jsonify, flash, url_for, request, render_template
from werkzeug.utils import redirect
from blueprints.utils import requer_login
from blueprints.documentos.controler import DocumentoControler
from blueprints.utils import upload_doc
from blueprints.forms import FormDocumento

bp = Blueprint("documentos", __name__)
documento_ctrl = DocumentoControler()


@bp.route("/admin/documentos")
@requer_login
def painel_documentos():
    pagina = request.args.get("page") or 1
    return render_template(
        "admin/painel-documentos.html",
        documentos=documento_ctrl.listar(apenas_ativos=False, pagina=pagina)
    )


@bp.route("/documentos", methods=["get", "post"])
def documentos():
    pagina = request.args.get("page") or 1
    tipo = request.args.get("tipo") or "Todos"
    termos = request.args.get("termos") or ""
    documentos = documento_ctrl.filtrar(pagina=pagina, tipo=tipo, termos=termos)

    return render_template(
        "/public/documentos.html", 
        documentos=documentos, 
        tipo=tipo, 
        termos=termos
    )


@bp.route("/admin/documentos/novo", methods=["GET", "POST"])
@requer_login
def novo():
    form = FormDocumento()
    if request.method == "POST":
        if form.validate_on_submit():
            doc_url = None
            if form.arquivo.data:
                doc_url = upload_doc(form.arquivo.data)
                if not doc_url:
                    flash(
                        "Ops.. erro no upload do arquivo. Por favor, verifique e tente novamente.",
                        "danger",
                    )
                    return render_template("admin/novo-documento.html", form=form)
            if documento_ctrl.cadastrar(
                tipo=form.tipo.data,
                titulo=form.titulo.data,
                url=doc_url,
                palavras_chave=form.palavras_chave.data,
            ):
                flash("Ok, novo documento cadastrado.", "success")
                return redirect(url_for("documentos.painel_documentos"))
            else:
                flash(
                    "Ops.. ocorreu um erro inesperado. Não foi possível cadastrar o documento. Por favor, tente outra vez."
                )
        else:
            flash(
                "Foram encontrados erros no formulário. Verifique e tente novamente.",
                "warning",
            )
        return render_template("admin/novo-documento.html", form=form)
    if request.method == "GET":
        return render_template("admin/novo-documento.html", form=form)


@bp.route("/admin/documentos/editar/<int:id>", methods=["GET", "POST"])
@requer_login
def editar(id):
    form = FormDocumento()
    documento = documento_ctrl.buscar_por_id(id)

    if request.method == "POST":
        if form.validate_on_submit():
            nova_url = None
            if form.arquivo.data:
                nova_url = upload_doc(form.arquivo.data)
                if not nova_url:
                    flash(
                        "Ocorreu um erro no upload do arquivo. Por favor, verifique e tente outra vez.",
                        category="danger",
                    )
                    return render_template("admin/editar-documento.html", form=form)
            print(f"Documentos->View->palavras_chave={form.palavras_chave.data}")
            if documento_ctrl.atualizar(
                id=form.id.data,
                tipo=form.tipo.data,
                titulo=form.titulo.data,
                url=nova_url,
                palavras_chave=form.palavras_chave.data,
            ):
                flash("Ok, documento atualizado.", category="success")
                return redirect(url_for("documentos.painel_documentos"))
            else:
                flash(
                    "Ops.. ocorreu um erro inesperado. As atualizações não foram salvas. Por favor, tente outra vez.",
                    category="danger",
                )
        else:
            flash(
                "Foram encontrados erros no formulário. Por favor, verifique e tente outra vez.",
                category="warning",
            )
        return render_template("admin/editar-documento.html", form=form)

    if request.method == "GET":
        if not documento:
            flash(
                "Erro, não foi possível carregar os dados do documento. Verifique e tente novamente.",
                "danger",
            )
            return redirect(url_for("documentos.painel_documentos"))

        form.id.data = documento.id
        form.tipo.data = documento.tipo
        form.titulo.data = documento.titulo
        form.arquivo.data = documento.url
        form.palavras_chave.data = documento.palavras_chave
        return render_template("admin/editar-documento.html", form=form)


@bp.route("/doc-atualizar-status", methods=["post"])
@requer_login
def atualizar_status():
    id = request.json.get("id")
    if documento_ctrl.atualizar_status(id):
        return jsonify({"sucesso": True, "id": id})
    return jsonify({"sucesso": False, "id": id})
