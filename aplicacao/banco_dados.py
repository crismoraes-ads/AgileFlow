
import os
import psycopg
from psycopg.rows import dict_row


def obter_conexao():
    url_banco = os.environ.get("DATABASE_URL")

    if not url_banco:
        raise RuntimeError(
            "A variável de ambiente DATABASE_URL não foi configurada."
        )

    return psycopg.connect(
        url_banco,
        row_factory=dict_row,
    )
