
from flask import Blueprint, request, redirect, url_for
from markupsafe import escape

from .banco_dados import obter_conexao

rotas = Blueprint("rotas", __name__)


@rotas.route("/")
def pagina_inicial():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head><meta charset="UTF-8"><title>AgileFlow</title></head>
    <body>
        <h1>AgileFlow</h1>
        <p>Gestão e acompanhamento de demandas de TI.</p>
        <a href="/demandas">Consultar demandas</a> |
        <a href="/demandas/nova">Registrar demanda</a>
    </body>
    </html>
    """


@rotas.route("/demandas")
def consultar_demandas():
    with obter_conexao() as conexao:
        demandas = conexao.execute(
            "SELECT id, titulo, descricao, status FROM demandas ORDER BY id"
        ).fetchall()

    lista = "".join(
        f"<li><strong>{escape(d['titulo'])}</strong> — "
        f"{escape(d['descricao'])} — Status: {escape(d['status'])}</li>"
        for d in demandas
    )

    if not lista:
        lista = "<li>Nenhuma demanda cadastrada.</li>"

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head><meta charset="UTF-8"><title>Consultar demandas</title></head>
    <body>
        <h1>Consultar demandas</h1>
        <ul>{lista}</ul>
        <a href="/">Voltar ao início</a> |
        <a href="/demandas/nova">Registrar demanda</a>
    </body>
    </html>
    """


@rotas.route("/demandas/nova", methods=["GET", "POST"])
def registrar_demanda():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not titulo or not descricao:
            return """
            <h1>Dados obrigatórios</h1>
            <p>Preencha o título e a descrição da demanda.</p>
            <a href="/demandas/nova">Voltar</a>
            """, 400

        with obter_conexao() as conexao:
            conexao.execute(
                "INSERT INTO demandas (titulo, descricao) VALUES (%s, %s)",
                (titulo, descricao),
            )

        return redirect(url_for("rotas.consultar_demandas"))

    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head><meta charset="UTF-8"><title>Registrar demanda</title></head>
    <body>
        <h1>Registrar demanda</h1>
        <form method="post">
            <label for="titulo">Título da demanda</label><br>
            <input id="titulo" name="titulo" maxlength="120" required><br><br>
            <label for="descricao">Descrição</label><br>
            <textarea id="descricao" name="descricao"
                      maxlength="1000" required></textarea><br><br>
            <button type="submit">Salvar demanda</button>
        </form>
        <a href="/">Voltar ao início</a>
    </body>
    </html>
    """
    
@rotas.route("/demandas/<int:id_demanda>/status", methods=["POST"])
def atualizar_status(id_demanda):
    novo_status = request.form.get("status", "").strip()
    status_permitidos = {"Aberta", "Em andamento", "Concluída"}

    if novo_status not in status_permitidos:
        return "Status inválido.", 400

    with obter_conexao() as conexao:
        resultado = conexao.execute(
            """
            UPDATE demandas
            SET status = %s
            WHERE id = %s
            RETURNING id
            """,
            (novo_status, id_demanda),
        ).fetchone()

    if resultado is None:
        return "Demanda não encontrada.", 404

    return redirect(url_for("rotas.consultar_demandas"))

@rotas.route(
    "/demandas/<int:id_demanda>/atualizacoes",
    methods=["GET", "POST"],
)
def registrar_atualizacao(id_demanda):
    if request.method == "POST":
        comentario = request.form.get("comentario", "").strip()

        if not comentario or len(comentario) > 1000:
            return "Comentário obrigatório (máximo de 1000 caracteres).", 400

        with obter_conexao() as conexao:
            demanda = conexao.execute(
                "SELECT id FROM demandas WHERE id = %s",
                (id_demanda,),
            ).fetchone()

            if demanda is None:
                return "Demanda não encontrada.", 404

            conexao.execute(
                """
                INSERT INTO atualizacoes (demanda_id, comentario)
                VALUES (%s, %s)
                """,
                (id_demanda, comentario),
            )

        return redirect(url_for("rotas.consultar_demandas"))

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head><meta charset="UTF-8"><title>Registrar atualização</title></head>
    <body>
        <h1>Registrar atualização</h1>
        <form method="post">
            <label for="comentario">Comentário / Atualização</label><br>
            <textarea id="comentario" name="comentario"
                      maxlength="1000" required></textarea><br><br>
            <button type="submit">Salvar atualização</button>
        </form>
        <a href="/">Voltar ao início</a>
    </body>
    </html>
    """

