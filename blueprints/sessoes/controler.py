from ext.database import con, Sessao
from flask import jsonify
from datetime import date
from dynaconf import settings


class SessaoControler:
    def cadastrar(self, tipo, data, hora, detalhes):
        try:
            nova_sessao = Sessao(tipo, data, hora, detalhes)
            con.session.add(nova_sessao)
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False

    def atualizar(self, id, tipo, data, hora, detalhes):
        try:
            sessao = self.buscar_por_id(id)
            sessao.tipo = tipo
            sessao.data = data
            sessao.hora = hora
            sessao.detalhes = detalhes
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False

    def atualizar_status(self, id):
        try:
            sessao = Sessao.query.get(id)
            sessao.status = not sessao.status
            con.session.commit()
            return jsonify({"sucesso": True, "id": sessao.id, "status": sessao.status})
        except Exception as erro:
            print(erro)
        return jsonify({"sucesso": False, "id": id})

    def listar_tudo(self, pagina=False, apenas_ativas=True):
        pagina = int(pagina) or 1

        if apenas_ativas:
            return (
                Sessao.query.filter(Sessao.status == True)
                .order_by(Sessao.data.desc())
                .paginate(pagina, settings.get("PAGINATION_OFFSET"))
            )

        return Sessao.query.order_by(Sessao.data.desc()).paginate(
            pagina, settings.get("PAGINATION_OFFSET")
        )

    def buscar_por_id(self, id):
        return Sessao.query.get(id)

    def proxima_sessao(self):
        return (
            con.session.query(Sessao)
            .filter(Sessao.status == True)
            .filter(Sessao.data >= date.today())
            .order_by(Sessao.data.asc())
            .first()
        )
