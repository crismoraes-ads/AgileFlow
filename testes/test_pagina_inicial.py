from importlib import import_module

from aplicacao import criar_aplicacao


def test_pagina_inicial():
    app = criar_aplicacao()
    resposta = app.test_client().get("/")
    assert resposta.status_code == 200
    assert b"AgileFlow" in resposta.data


def test_consultar_demandas(monkeypatch):
    modulo_rotas = import_module("aplicacao.rotas")

    class BancoFalso:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def execute(self, *args):
            class Resultado:
                def fetchall(self):
                    return []

            return Resultado()

    monkeypatch.setattr(modulo_rotas, "obter_conexao", BancoFalso)

    app = criar_aplicacao()
    resposta = app.test_client().get("/demandas")

    assert resposta.status_code == 200
    assert b"Nenhuma demanda cadastrada" in resposta.data


def test_formulario_nova_demanda():
    app = criar_aplicacao()
    resposta = app.test_client().get("/demandas/nova")
    assert resposta.status_code == 200
    assert b"Registrar demanda" in resposta.data
