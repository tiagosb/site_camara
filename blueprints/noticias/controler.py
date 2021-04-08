from datetime import datetime
from flask.json import jsonify
from ext.database import con, Noticia
from dynaconf import settings


class NoticiasControler:

    def listar_tudo(self, pagina=False, apenas_ativas=True, apenas_destacadas=False):
        pagina = int(pagina)
        if not pagina and apenas_destacadas:
            return Noticia.query.order_by(Noticia.postado_em.desc()).filter(Noticia.status == True).filter(Noticia.destaque == True)

        if apenas_ativas:
            return Noticia.query.order_by(Noticia.postado_em.desc()).filter(Noticia.status == True).paginate(
                pagina, settings.get("PAGINATION_OFFSET")
            )

        return Noticia.query.order_by(Noticia.postado_em.desc()).paginate(pagina, settings.get("PAGINATION_OFFSET"))

    def buscar_por_id(self, id):
        return Noticia.query.get(id)

    def cadastrar(self, titulo, conteudo, thumb_url, categoria, destaque):
        try:
            nova_noticia = Noticia(titulo, conteudo, thumb_url, categoria, destaque)
            con.session.add(nova_noticia)
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
            return False

    def atualizar(self, id, titulo, conteudo, thumb_url, categoria, destaque):
        try:
            noticia = self.buscar_por_id(id)
            noticia.titulo = titulo
            noticia.conteudo = conteudo
            noticia.categoria = categoria
            noticia.destaque = destaque
            if thumb_url:
                noticia.thumb = thumb_url
            noticia.atualizado_em = datetime.now()
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
            return False

    def atualizar_status(self, id):
        try:
            noticia = self.buscar_por_id(id)
            noticia.status = not noticia.status
            con.session.commit()
            return jsonify(
                {"sucesso": True, "id": noticia.id, "status": noticia.status}
            )
        except Exception as erro:
            print(erro)
            return jsonify({"sucesso": False, "id": id})
