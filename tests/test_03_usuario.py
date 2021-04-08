from flask import session, request

usuario = "test@test"
senha = "test"


def test_deve_cadastrar_usuario_e_retornar_json_com_key_sucesso_igual_a_true(client):
    cadastro = client.post(
        "/usuarios/cadastrar", data=dict(usuario=usuario, senha=senha)
    )
    assert cadastro.json.get("sucesso") == True


def test_deve_retornar_usuario_inexistente(client):
    response = client.post("/login", data=dict(usuario=usuario + "x", senha=senha))
    assert "Usuário inexistente.".encode() in response.data


def test_deve_retornar_senha_incorreta(client):
    response = client.post("/login", data=dict(usuario=usuario, senha=senha + "x"))
    assert b"Senha incorreta." in response.data


def test_deve_setar_session_auth_igual_a_true_e_redirecionar_para_rota_admin(client):
    login = client.post("/login", data=dict(usuario=usuario, senha=senha))
    assert "auth" in session and session["auth"] == True
    assert login.location == "http://localhost/admin"
