from flask_sqlalchemy import SQLAlchemy
import datetime


con = SQLAlchemy()


def init_app(app):
    con.init_app(app)


class Sessao(con.Model):
    id = con.Column(con.Integer, primary_key=True, autoincrement=True)
    tipo = con.Column(con.Integer)
    data = con.Column(con.Date)
    hora = con.Column(con.Time)
    detalhes = con.Column(con.Text)
    status = con.Column(con.Boolean, default=True)
    postado_em = con.Column(con.DateTime, default=datetime.datetime.now)
    atualizado_em = con.Column(con.DateTime, default=None)

    def __init__(self, tipo, data, hora, detalhes):
        self.tipo = tipo
        self.data = data
        self.hora = hora
        self.detalhes = detalhes


class Usuario(con.Model):
    id = con.Column(con.Integer, primary_key=True, autoincrement=True)
    usuario = con.Column(con.String(250), unique=True)
    senha = con.Column(con.String(250))

    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha


class Noticia(con.Model):
    id = con.Column(con.Integer, primary_key=True, autoincrement=True)
    titulo = con.Column(con.String(250))
    categoria = con.Column(con.String(250))
    conteudo = con.Column(con.Text)
    thumb = con.Column(con.String(250))
    status = con.Column(con.Boolean, default=True)
    postado_em = con.Column(con.DateTime, default=datetime.datetime.now)
    atualizado_em = con.Column(con.DateTime, default=None)
    destaque = con.Column(con.Boolean, default=False)

    def __init__(self, titulo, conteudo, thumb=None, categoria=None, destaque=False):
        self.titulo = titulo
        self.conteudo = conteudo
        self.thumb = thumb
        self.categoria = categoria
        self.destaque = destaque


class Vereador(con.Model):
    id = con.Column(con.Integer, primary_key=True, autoincrement=True)
    nome_civil = con.Column(con.String(250))
    nome_urna = con.Column(con.String(250))
    naturalidade = con.Column(con.String(250))
    uf = con.Column(con.String(250))
    ocupacao = con.Column(con.String(250))
    escolaridade = con.Column(con.String(250))
    partido = con.Column(con.String(250))
    legislaturas = con.Column(con.String(250))
    telefone = con.Column(con.String(250))
    email = con.Column(con.String(250))
    nascimento = con.Column(con.Date)
    detalhes = con.Column(con.String(250))
    foto = con.Column(con.String(250))
    status = con.Column(con.Boolean, default=True)
    postado_em = con.Column(con.DateTime, default=datetime.datetime.now)

    def __init__(
        self,
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
    ):
        self.nome_civil = nome_civil
        self.nome_urna = nome_urna
        self.naturalidade = naturalidade
        self.uf = uf
        self.ocupacao = ocupacao
        self.escolaridade = escolaridade
        self.partido = partido
        self.legislaturas = legislaturas
        self.telefone = telefone
        self.email = email
        self.nascimento = nascimento
        self.detalhes = detalhes
        self.foto = foto


class Diaria(con.Model):
    id = con.Column(con.Integer, primary_key=True, autoincrement=True)
    nome = con.Column(con.String(250))
    data = con.Column(con.Date)
    destino = con.Column(con.String(250))
    motivo = con.Column(con.String(250))
    valor = con.Column(con.String(250))
    postado_em = con.Column(con.DateTime, default=datetime.datetime.now)

    def __init__(self, nome, data, destino, motivo, valor):
        self.nome = nome
        self.data = data
        self.destino = destino
        self.motivo = motivo
        self.valor = valor


class Documento(con.Model):
    id = con.Column(con.Integer, primary_key=True, autoincrement=True)
    titulo = con.Column(con.String(250))
    tipo = con.Column(con.String(250))
    url = con.Column(con.String(250))
    status = con.Column(con.Boolean, default=True)
    postado_em = con.Column(con.DateTime, default=datetime.datetime.now)
    palavras_chave = con.Column(con.String(250), default="")

    def __init__(self, titulo, tipo, url, palavras_chave):
        self.titulo = titulo
        self.tipo = tipo
        self.url = url
        self.palavras_chave = palavras_chave

