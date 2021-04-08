from ext.database import con, Diaria
from dynaconf import settings


class DiariaControler:
    def listar_tudo(self, pagina):
        pagina = int(pagina) or 1
        return Diaria.query.order_by(Diaria.postado_em.desc()).paginate(pagina, settings.get("PAGINATION_OFFSET"))

    def consultar_por_id(self, id):
        return Diaria.query.get(id)

    def cadastrar(self, nome, data, destino, motivo, valor):
        try:
            nova_diaria = Diaria(nome, data, destino, motivo, valor)
            con.session.add(nova_diaria)
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False

    def atualizar(self, id, nome, data, destino, motivo, valor):
        try:
            diaria = self.consultar_por_id(id)
            diaria.nome = nome
            diaria.data = data
            diaria.destino = destino
            diaria.motivo = motivo
            diaria.valor = valor
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False
