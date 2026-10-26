import os

import psycopg


def obter_conexao():
    url_banco = os.environ.get("DATABASE_URL")

    if not url_banco:
        raise RuntimeError(
            "A variável de ambiente DATABASE_URL não foi configurada."
        )

    return psycopg.connect(url_banco)


def criar_tabela_demandas():
    with obter_conexao() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS demandas (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                titulo VARCHAR(120) NOT NULL,
                descricao VARCHAR(1000) NOT NULL,
                status VARCHAR(30) NOT NULL DEFAULT 'Aberta'
            )
        """)
