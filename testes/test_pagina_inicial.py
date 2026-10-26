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
    
def test_atualizar_status_demanda(monkeypatch):
    from importlib import import_module

    modulo_rotas = import_module("aplicacao.rotas")

    class BancoFalso:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def execute(self, comando, parametros):
            assert "UPDATE demandas" in comando
            assert parametros == ("Em andamento", 1)

            class Resultado:
                def fetchone(self):
                    return (1,)

            return Resultado()

    monkeypatch.setattr(modulo_rotas, "obter_conexao", BancoFalso)

    app = criar_aplicacao()
    resposta = app.test_client().post(
        "/demandas/1/status",
        data={"status": "Em andamento"},
    )

    assert resposta.status_code == 302
    assert resposta.location.endswith("/demandas")


def test_atualizar_status_invalido():
    app = criar_aplicacao()
    resposta = app.test_client().post(
        "/demandas/1/status",
        data={"status": "Status inventado"},
    )

    assert resposta.status_code == 400

