from aplicacao import criar_aplicacao


def test_pagina_inicial():
    app = criar_aplicacao()
    resposta = app.test_client().get("/")
    assert resposta.status_code == 200
    assert b"AgileFlow" in resposta.data


def test_consultar_demandas():
    app = criar_aplicacao()
    resposta = app.test_client().get("/demandas")
    assert resposta.status_code == 200
    assert b"Nenhuma demanda cadastrada" in resposta.data


def test_formulario_nova_demanda():
    app = criar_aplicacao()
    resposta = app.test_client().get("/demandas/nova")
    assert resposta.status_code == 200
    assert b"Registrar demanda" in resposta.data
