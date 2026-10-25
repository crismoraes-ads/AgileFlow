from aplicacao import criar_aplicacao


def test_pagina_inicial():
    aplicacao = criar_aplicacao()
    cliente = aplicacao.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"AgileFlow" in resposta.data
