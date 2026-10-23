
from flask import Blueprint

rotas = Blueprint("rotas", __name__)


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
    </body>
    </html>
    """
