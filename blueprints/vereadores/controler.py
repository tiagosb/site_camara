from flask.json import jsonify
from sqlalchemy.sql.elements import True_
from ext.database import con, Vereador
from flask import abort
from dynaconf import settings


class VereadorControler:
    def buscar_por_id(self, id):
        return Vereador.query.get(id)

    def listar_todos(self, pagina=1, apenas_ativos=True):
        """
        Retorna todos os vereadores ativos se apenas_ativos for True
        caso contrário retorna todos os vereadores ativos e inativos
        (objeto Paginate retornado)
        """
        pagina = int(pagina)
        if apenas_ativos:
            return Vereador.query.order_by(Vereador.postado_em.desc()).filter(Vereador.status == True).paginate(
                pagina, settings.get("PAGINATION_OFFSET")
            )
        return Vereador.query.order_by(Vereador.postado_em.desc()).paginate(pagina, settings.get("PAGINATION_OFFSET"))

    def listar_todos_sem_paginacao(self):
        """
        Retorna todos os vereadores ativos para exibição no slide de vereadores.
        (lista retornada)
        """
        return Vereador.query.order_by(Vereador.postado_em.desc()).all()

    def cadastrar(
        self,
        nascimento,
        nome_civil,
        nome_urna,
        naturalidade,
        uf,
        ocupacao,
        escolaridade,
        partido,
        legislaturas,
        telefone,
        email,
        detalhes,
        foto,
    ):
        try:
            novo_vereador = Vereador(
                nome_civil,
                nome_urna,
                naturalidade,
                uf,
                ocupacao,
                escolaridade,
                partido,
                legislaturas,
                telefone,
                email,
                nascimento,
                detalhes,
                foto,
            )
            con.session.add(novo_vereador)
            con.session.commit()
            return True
        except Exception as erro:
            print(erro)
        return False

    def atualizar_status(self, id):
        try:
            vereador = self.buscar_por_id(id)
            vereador.status = not vereador.status
            con.session.commit()
            return jsonify(
                {"sucesso": True, "id": vereador.id, "status": vereador.status}
            )
        except Exception as erro:
            print(erro)
        return jsonify({"sucesso": False, "id": id})

    def atualizar(
        self,
        id,
        nascimento,
        nome_civil,
        nome_urna,
        naturalidade,
        uf,
        ocupacao,
        escolaridade,
        partido,
        legislaturas,
        telefone,
        email,
        detalhes,
        foto,
    ):
        try:
            vereador = self.buscar_por_id(id)
            vereador.nascimento = nascimento
            vereador.nome_civil = nome_civil
            vereador.nome_urna = nome_urna
            vereador.naturalidade = naturalidade
            vereador.uf = uf
            vereador.ocupacao = ocupacao
            vereador.escolaridade = escolaridade
            vereador.partido = partido
            vereador.legislaturas = legislaturas
            vereador.telefone = telefone
            vereador.email = email
            vereador.detalhes = detalhes
            if foto:
                vereador.foto = foto
            con.session.commit()
            print("Ok, as alteracoes foram salvas.")
            return True
        except Exception as erro:
            print(erro)
        return False
