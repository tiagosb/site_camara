from sqlalchemy import or_
from ext.database import con, Documento
from dynaconf import settings


class DocumentoControler:
    def cadastrar(self, tipo, titulo, url, palavras_chave):
        try:
            novo_documento = Documento(
                tipo=tipo, titulo=titulo, url=url, palavras_chave=palavras_chave
            )
            con.session.add(novo_documento)
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False

    def atualizar(self, id, tipo, titulo, url, palavras_chave):
        try:
            documento = self.buscar_por_id(id)
            documento.tipo = tipo
            documento.titulo = titulo
            documento.palavras_chave = palavras_chave
            if url:
                documento.url = url
            con.session.commit()
            return True
        except Exception as erro:
            con.session.rollback()
            print(erro)
        return False

    def atualizar_status(self, id):
        try:
            documento = Documento.query.get(id)
            documento.status = not documento.status
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False

    def buscar_por_id(self, id):
        return Documento.query.get(id)

    def listar(self, pagina, apenas_ativos=True):
        pagina = int(pagina)
        if apenas_ativos:
            return Documento.query.order_by(Documento.postado_em.desc()).filter(Documento.status == True).paginate(
                pagina, settings.get("PAGINATION_OFFSET")
            )
        return Documento.query.order_by(Documento.postado_em.desc()).paginate(pagina, settings.get("PAGINATION_OFFSET"))

    def filtrar(self, pagina, tipo, termos):
        pagina = int(pagina)
        termos = f"%{termos}%"
        if tipo.lower() == "todos":
            return Documento.query.filter(
                or_(
                    Documento.titulo.like(termos), Documento.palavras_chave.like(termos)
                )
            ).paginate(pagina, settings.get("PAGINATION_OFFSET"))
        return (
            Documento.query.filter(Documento.tipo == tipo)
            .filter(Documento.palavras_chave.like(termos))
            .paginate(pagina, settings.get("PAGINATION_OFFSET"))
        )
