from flask import session

rotas_protegidas = [
    "/admin",
    "/admin/noticias",
    "/admin/noticias/nova",
    "/admin/documentos",
    "/admin/documentos/novo",
    "/admin/vereadores",
    "/admin/vereadores/novo",
    "/admin/diarias",
    "/admin/diarias/nova",
    "/admin/sessoes",
    "/admin/sessoes/nova",
]


def test_deve_redirecionar_para_login_ao_acessar_rotas_protegidas(client):
    for rota in rotas_protegidas:
        assert client.get(rota).status_code == 302
