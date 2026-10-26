import os

import psycopg


def obter_conexao():
    url_banco = os.environ.get("DATABASE_URL")

    if not url_banco:
        raise RuntimeError(
            "A variável de ambiente DATABASE_URL não foi configurada."
        )

    return psycopg.connect(url_banco)
