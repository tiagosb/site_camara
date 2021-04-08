from dynaconf import settings
from .utils import requer_login, upload_image
from flask import Blueprint, request, url_for, jsonify


bp = Blueprint("upload", __name__)


@bp.route("/upl", methods=["get", "post"])
@requer_login
def upl():
    try:
        arquivo = request.files.get("file")
        if arquivo:
            nome = upload_image(arquivo)
            if nome:
                return (
                    jsonify({"location": url_for("views.media_img", filename=nome)}),
                    200,
                )
        return jsonify({"location": ""}), 405
    except Exception as err:
        print(err)
        return jsonify({"location": ""}), 500
