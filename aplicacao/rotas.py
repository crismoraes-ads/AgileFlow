
from flask import Blueprint, request, redirect, url_for

rotas = Blueprint("rotas", __name__)

# Armazenamento temporário durante a execução da aplicação.
demandas = []
proximo_id = 1


@rotas.route("/")
def pagina_inicial():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AgileFlow</title>
    </head>
    <body>
        <h1>AgileFlow</h1>
        <p>Gestão e acompanhamento de demandas de TI.</p>
        <p>Bem-vindo ao sistema!</p>

        <nav>
            <a href="/demandas">Consultar demandas</a>
            |
            <a href="/demandas/nova">Registrar demanda</a>
        </nav>
    </body>
    </html>
    """


@rotas.route("/demandas")
def consultar_demandas():
    lista = ""

    for demanda in demandas:
        lista += f"""
        <li>
            <strong>{demanda['titulo']}</strong>
            — {demanda['descricao']}
            — Status: {demanda['status']}
        </li>
        """

    if not lista:
        lista = "<li>Nenhuma demanda cadastrada.</li>"

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Consultar demandas - AgileFlow</title>
    </head>
    <body>
        <h1>Consultar demandas</h1>
        <ul>{lista}</ul>
        <a href="/">Voltar ao início</a>
        |
        <a href="/demandas/nova">Registrar demanda</a>
    </body>
    </html>
    """


@rotas.route("/demandas/nova", methods=["GET", "POST"])
def registrar_demanda():
    global proximo_id

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if titulo and descricao:
            demandas.append({
                "id": proximo_id,
                "titulo": titulo,
                "descricao": descricao,
                "status": "Aberta"
            })
            proximo_id += 1
            return redirect(url_for("rotas.consultar_demandas"))

        return """
        <h1>Dados obrigatórios</h1>
        <p>Preencha o título e a descrição da demanda.</p>
        <a href="/demandas/nova">Voltar ao formulário</a>
        """

    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registrar demanda - AgileFlow</title>
    </head>
    <body>
        <h1>Registrar demanda</h1>

        <form method="post">
            <label for="titulo">Título da demanda</label><br>
            <input id="titulo" name="titulo" type="text"
                   maxlength="120" required><br><br>

            <label for="descricao">Descrição</label><br>
            <textarea id="descricao" name="descricao"
                      maxlength="1000" required></textarea><br><br>

            <button type="submit">Salvar demanda</button>
        </form>

        <p><a href="/">Voltar ao início</a></p>
    </body>
    </html>
    """
