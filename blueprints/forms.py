from flask_wtf import FlaskForm
from wtforms.fields.core import DateField, SelectField, StringField
from wtforms.fields.simple import FileField, HiddenField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, Regexp
from wtforms.fields.html5 import (
    DateField,
    DecimalField,
    EmailField,
    TelField,
    TimeField,
)


class FormVereador(FlaskForm):
    id = HiddenField(validators=[Optional()])
    nome_civil = StringField("Nome Civil", validators=[DataRequired()])
    nome_urna = StringField("Nome de Urna", validators=[DataRequired()])
    naturalidade = StringField("Naturalidade", validators=[DataRequired()])
    uf = StringField("UF", validators=[DataRequired()])
    ocupacao = StringField("Ocupação", validators=[DataRequired()])
    escolaridade = SelectField(
        "Escolaridade",
        choices=[
            ("Ensino Fundamental", "Ensino Fundamental"),
            ("Ensino Médio", "Ensino Médio"),
            ("Ensino Superior", "Ensino Superior"),
        ],
        default="Ensino Médio",
    )
    partido = StringField("Partido", validators=[DataRequired()])
    legislaturas = StringField("Legislatura", validators=[DataRequired()])
    telefone = TelField("Telefone", validators=[Optional()])
    email = EmailField("E-mail", validators=[Optional()])
    nascimento = DateField("Data de Nascimento", validators=[DataRequired()])
    detalhes = TextAreaField("Detalhes", validators=[Optional()])
    thumb = FileField("Fotografia", validators=[Optional()])


class FormDocumento(FlaskForm):
    id = HiddenField(validators=[Optional()])
    titulo = StringField("Título do documento", validators=[DataRequired()])
    tipo = SelectField(
        "Tipo de documento",
        choices=[
            ("Lei", "Lei"),
            ("Projeto de lei", "Projeto de lei"),
            ("Decreto", "Decreto"),
        ],
        default="Lei",
    )
    arquivo = FileField("Documento", validators=[Optional()])
    palavras_chave = StringField("Palavras de busca", validators=[DataRequired()])


class FormDiaria(FlaskForm):
    id = HiddenField(validators=[Optional()])
    nome = StringField("Nome", validators=[DataRequired()])
    data = DateField("Data", validators=[DataRequired()])
    destino = StringField("Destino", validators=[DataRequired()])
    motivo = StringField("Motivo", validators=[DataRequired()])
    valor = DecimalField("Valor", validators=[DataRequired()])


class FormSessao(FlaskForm):
    id = HiddenField(validators=[Optional()])
    tipo = SelectField(
        "Tipo de sessão",
        choices=[
            ("Sessão Ordinária", "Sessão Ordinária"),
            ("Audiência Pública", "Audiência Pública"),
        ],
        default="Sessão Ordinária",
    )

    data = DateField("Data da sessão", validators=[DataRequired()])
    hora = TimeField("Hora da sessão", validators=[DataRequired()])
    detalhes = TextAreaField("Detalhes/Pauta")


class FormLogin(FlaskForm):
    id = HiddenField(validators=[Optional()])
    usuario = StringField(
        "Usuário",
        [
            DataRequired(message="Informe seu usuário."),
            Length(5, 50, message="Deve ter pelo menos 5 caracteres."),
            Regexp(r"^[\w.@+-]+$"),
        ],
    )
    senha = PasswordField(
        "Senha",
        [
            DataRequired(message="Informe sua senha."),
            Length(4, 15, message="De 4 a 15 caracteres."),
            Regexp(r"^[\w.@+-]+$"),
        ],
    )


class FormNoticia(FlaskForm):
    id = HiddenField(validators=[Optional()])
    categoria = SelectField(
        "Categoria",
        choices=[
            ("Geral", "Geral"),
            ("Segurança", "Segurança"),
            ("Saúde", "Saúde"),
            ("Economia", "Economia"),
        ],
        default="Geral",
    )

    titulo = StringField(
        "Título",
        [
            DataRequired(message="Informe título da notícia."),
            Length(5, 150, message="Deve ter pelo menos 5 caracteres."),
        ],
    )

    conteudo = TextAreaField("Conteúdo")

    destaque = SelectField(
        "Destacar na página inicial?",
        choices=[("sim", "Sim"), ("nao", "Não")],
        default="nao",
    )

    thumb = FileField("Imagem de capa da notícia", validators=[Optional()])
