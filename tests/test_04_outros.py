# noticias
from flask import json


def test_deve_cadastrar_nova_noticia(client):
    # faz login primeiro
    client.post("/login", data=dict(usuario="test@test", senha="test"))
    response = client.post(
        "/admin/noticias/nova",
        data=dict(
            categoria="Geral",
            titulo="Titulo da Primeira Noticia",
            conteudo="Esse é o conteúdo da primeira notícia.",
            destaque="nao",
            thumb=None,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Ok! A noticia foi cadastrada".encode() in response.data


# assumindo que o id da noticia cadastrada acima será 1
def test_deve_editar_noticia(client):
    # Faz login antes de acessar uma rota protegida
    client.post("/login", data=dict(usuario="test@test", senha="test"))
    response = client.post(
        "/admin/noticias/editar/1",
        data=dict(
            id=1,
            categoria="Economia",
            titulo="Titulo da Primeira Noticia Editado",
            conteudo="Esse é o conteúdo da primeira notícia, ele foi editado.",
            destaque="nao",
            thumb=None,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Ok, a noticia foi atualizada" in response.data


def test_deve_alterar_o_status_da_noticia(client):
    client.post("/login", data=dict(usuario="test@test", senha="test"))

    response = client.post(
        "/admin/noticias/alterar-status",
        data=json.dumps(dict(id=1)),
        content_type="application/json",
    )

    assert response.json.get("sucesso") == True
