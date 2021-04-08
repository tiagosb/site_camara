import click
from ext.database import con, Noticia, Usuario, Sessao, Vereador, Diaria, Documento
import bcrypt


def init_app(app):
    @app.cli.command("create-db")
    def create_db():
        try:
            con.create_all()
            senha_hash = bcrypt.hashpw(b"admin", bcrypt.gensalt())
            user_admin = Usuario("admin@admin", senha_hash)
            con.session.add(user_admin)
            con.session.commit()
            click.echo("Ok, banco de dados pronto para uso.")
        except Exception as erro:
            click.echo(erro)
