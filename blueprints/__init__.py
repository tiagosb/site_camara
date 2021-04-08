from .diarias.view import bp as diaria_bp
from .documentos.view import bp as documento_bp
from .noticias.view import bp as noticia_bp
from .sessoes.view import bp as sessao_bp
from .vereadores.view import bp as vereador_bp
from .views import bp as views_bp
from .usuario import bp as usuario_bp
from .services import bp as services_bp


def init_app(app):
    app.register_blueprint(diaria_bp)
    app.register_blueprint(documento_bp)
    app.register_blueprint(noticia_bp)
    app.register_blueprint(sessao_bp)
    app.register_blueprint(vereador_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(services_bp)
