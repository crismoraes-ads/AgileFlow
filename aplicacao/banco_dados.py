
import os

import psycopg


def obter_conexao():
    url_banco = os.environ.get("DATABASE_URL")

    if not url_banco:
        raise RuntimeError(
            "A variável de ambiente DATABASE_URL não foi configurada."
        )

   return psycopg.connect(
    url_banco,
    row_factory=psycopg.rows.dict_row,
)


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


def criar_tabela_atualizacoes():
    with obter_conexao() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS atualizacoes (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                demanda_id INTEGER NOT NULL REFERENCES demandas(id)
                    ON DELETE CASCADE,
                comentario VARCHAR(1000) NOT NULL,
                data_atualizacao DATE NOT NULL DEFAULT CURRENT_DATE
            )
        """)
