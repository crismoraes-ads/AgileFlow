
from flask import Blueprint, request, redirect, url_for
from markupsafe import escape

from .banco_dados import obter_conexao


rotas = Blueprint("rotas", __name__)

STATUS_PERMITIDOS = ("Aberta", "Em andamento", "Concluída")


def _pagina(titulo, conteudo):
    """Monta uma página com estilo e controles de acessibilidade comuns."""
    modelo = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>AgileFlow | %%TITULO%%</title>
        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                background: #f3f6fa;
                color: #202b3c;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 16px;
                line-height: 1.6;
            }

            .container {
                width:  min(960px, 92%);
                margin: 0 auto;
            }

            header {
                background: #ffffff;
                border-bottom: 2px solid #d8e1ec;
                padding: 20px 0;
            }

            .marca {
                color: #163b65;
                font-size: 1.8em;
                font-weight: bold;
                text-decoration: none;
            }

            .subtitulo {
                margin: 4px 0 18px;
            }

            main {
                padding-top: 28px;
                padding-bottom: 40px;
            }

            h1 {
                color: #163b65;
                font-size: 1.8em;
                line-height: 1.3;
            }

            h2 {
                color: #163b65;
                font-size: 1.35em;
                line-height: 1.4;
            }

            h3 {
                font-size: 1.1em;
            }

            p {
                overflow-wrap: anywhere;
            }

            .painel,
            .demanda,
            .acessibilidade {
                background: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 20px;
                margin: 18px 0;
            }

            .acessibilidade {
                border: 2px solid #536579;
            }

            .acessibilidade h2 {
                margin-top: 0;
            }

            .acoes,
            .navegacao {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin-top: 18px;
            }

            a {
                color: #064f91;
                text-decoration: underline;
                text-underline-offset: 3px;
            }

            .botao-link,
            button {
                display: inline-block;
                border: 2px solid #194b79;
                border-radius: 6px;
                padding: 10px 14px;
                background: #194b79;
                color: #ffffff;
                font: inherit;
                font-weight: bold;
                text-align: center;
                text-decoration: none;
                cursor: pointer;
            }

            .botao-secundario,
            button.secundario {
                background: #ffffff;
                color: #194b79;
            }

            a:focus-visible,
            button:focus-visible,
            input:focus-visible,
            textarea:focus-visible,
            select:focus-visible {
                outline: 3px solid #e09b00;
                outline-offset: 4px;
            }

            label {
                display: block;
                font-weight: bold;
                margin: 14px 0 6px;
            }

            input,
            textarea,
            select {
                width: 100%;
                max-width: 100%;
                padding: 10px;
                border: 1px solid #68788a;
                border-radius: 5px;
                background: #ffffff;
                color: #202b3c;
                font: inherit;
            }

            textarea {
                min-height: 130px;
                resize: vertical;
            }

            .campo {
                margin-bottom: 16px;
            }

            .formulario {
                max-width: 700px;
            }

            .form-status {
                display: flex;
                flex-wrap: wrap;
                align-items: end;
                gap: 12px;
                margin-top: 14px;
            }

            .form-status .campo {
                flex: 1 1 220px;
                margin: 0;
            }

            .form-status label {
                margin-top: 0;
            }

            .status {
                display: inline-block;
                padding: 3px 9px;
                border: 1px solid #73849a;
                border-radius: 5px;
                font-weight: bold;
            }

            .historico {
                padding-left: 24px;
            }

            .historico li {
                margin-bottom: 10px;
                overflow-wrap: anywhere;
            }

            .texto-suave {
                color: #49596b;
            }

            .pular-conteudo {
                position: absolute;
                top: -100px;
                left: 12px;
                background: #ffffff;
                padding: 10px;
                z-index: 10;
            }

            .pular-conteudo:focus {
                top: 12px;
            }

            footer {
                padding: 20px 0;
                border-top: 1px solid #cbd5e1;
                color: #49596b;
            }

            @media (max-width: 600px) {
                .painel,
                .demanda,
                .acessibilidade {
                    padding: 14px;
                }

                .botao-link,
                button {
                    max-width: 100%;
                }
            }
        </style>
    </head>
    <body>
        <a class="pular-conteudo" href="#conteudo">
            Pular para o conteúdo principal
        </a>

        <header>
            <div class="container">
                <a class="marca" href="/">AgileFlow</a>
                <p class="subtitulo">
                    Gestão e acompanhamento de demandas de TI
                </p>

                <section class="acessibilidade"
                         aria-labelledby="titulo-acessibilidade">
                    <h2 id="titulo-acessibilidade">
                        Acessibilidade: tamanho do texto
                    </h2>
                    <p>
                        Ajuste o tamanho das letras para facilitar a leitura.
                    </p>
                    <div class="acoes">
                        <button type="button"
                                class="secundario"
                                aria-label="Diminuir tamanho do texto"
                                onclick="alterarTamanhoTexto(-2)">
                            A− Diminuir
                        </button>
                        <button type="button"
                                aria-label="Aumentar tamanho do texto"
                                onclick="alterarTamanhoTexto(2)">
                            A+ Aumentar
                        </button>
                        <button type="button"
                                class="secundario"
                                onclick="restaurarTamanhoTexto()">
                            Restaurar
                        </button>
                    </div>
                </section>
            </div>
        </header>

        <main id="conteudo" class="container">
            %%CONTEUDO%%
        </main>

        <footer>
            <div class="container">
                <p>AgileFlow — MVP de gestão e acompanhamento de demandas.</p>
            </div>
        </footer>

        <script>
            function alterarTamanhoTexto(variacao) {
                const corpo = document.body;
                const atual = parseFloat(
                    window.getComputedStyle(corpo).fontSize
                );
                const novo = Math.max(14, Math.min(28, atual + variacao));

                corpo.style.fontSize = novo + "px";
            }

            function restaurarTamanhoTexto() {
                document.body.style.fontSize = "16px";
            }
        </script>
    </body>
    </html>
    """

    return (
        modelo
        .replace("%%TITULO%%", str(escape(titulo)))
        .replace("%%CONTEUDO%%", conteudo)
    )


@rotas.route("/")
def pagina_inicial():
    conteudo = """
    <section class="painel">
        <h1>Bem-vindo ao AgileFlow</h1>
        <p>
            Organize e acompanhe as demandas de TI em um único lugar.
            Consulte solicitações, atualize o andamento e registre comentários.
        </p>

        <nav class="acoes" aria-label="Funcionalidades principais">
            <a class="botao-link" href="/demandas">
                Consultar demandas
            </a>
            <a class="botao-link botao-secundario" href="/demandas/nova">
                Registrar demanda
            </a>
        </nav>
    </section>
    """

    return _pagina("Início", conteudo)


@rotas.route("/demandas")
def consultar_demandas():
    with obter_conexao() as conexao:
        demandas = conexao.execute(
            """
            SELECT id, titulo, descricao, status
            FROM demandas
            ORDER BY id
            """
        ).fetchall()

        blocos = []

        for demanda in demandas:
            identificador = demanda["id"]

            atualizacoes = conexao.execute(
                """
                SELECT comentario, data_atualizacao
                FROM atualizacoes
                WHERE demanda_id = %s
                ORDER BY data_atualizacao DESC, id DESC
                """,
                (identificador,),
            ).fetchall()

            itens_historico = "".join(
                "<li>"
                f"<strong>{escape(str(item['data_atualizacao']))}</strong>"
                " — "
                f"{escape(item['comentario'])}"
                "</li>"
                for item in atualizacoes
            )

            if not itens_historico:
                itens_historico = (
                    "<li>Nenhuma atualização registrada.</li>"
                )

            opcoes_status = ""

            for status in STATUS_PERMITIDOS:
                selecionado = (
                    " selected"
                    if status == demanda["status"]
                    else ""
                )
                opcoes_status += (
                    f'<option value="{escape(status)}"{selecionado}>'
                    f"{escape(status)}</option>"
                )

            formulario_status = (
                '<form class="form-status" method="post" '
                f'action="{url_for("rotas.atualizar_status", id_demanda=identificador)}">'
                '<div class="campo">'
                f'<label for="status-{identificador}">Alterar status</label>'
                f'<select id="status-{identificador}" name="status" required>'
                f"{opcoes_status}"
                "</select>"
                "</div>"
                '<button type="submit">Salvar status</button>'
                "</form>"
            )

            link_atualizacao = (
                '<p><a class="botao-link botao-secundario" '
                f'href="{url_for("rotas.registrar_atualizacao", id_demanda=identificador)}">'
                "Registrar atualização</a></p>"
            )

            bloco = (
                '<article class="demanda">'
                f"<h2>{escape(demanda['titulo'])}</h2>"
                f"<p>{escape(demanda['descricao'])}</p>"
                "<p><strong>Status atual:</strong> "
                f'<span class="status">{escape(demanda["status"])}</span></p>'
                f"{formulario_status}"
                f"{link_atualizacao}"
                "<h3>Histórico de atualizações</h3>"
                f'<ul class="historico">{itens_historico}</ul>'
                "</article>"
            )

            blocos.append(bloco)

    if blocos:
        lista_demandas = "".join(blocos)
    else:
        lista_demandas = (
            '<section class="painel">'
            "<p>Nenhuma demanda cadastrada.</p>"
            '<p><a href="/demandas/nova">Registrar a primeira demanda</a></p>'
            "</section>"
        )

    conteudo = (
        "<h1>Consultar demandas</h1>"
        "<p>Consulte as solicitações, altere seus status "
        "e registre atualizações.</p>"
        f"{lista_demandas}"
        '<nav class="navegacao" aria-label="Navegação">'
        '<a href="/">Voltar ao início</a>'
        '<a href="/demandas/nova">Registrar demanda</a>'
        "</nav>"
    )

    return _pagina("Consultar demandas", conteudo)


@rotas.route("/demandas/nova", methods=["GET", "POST"])
def registrar_demanda():
    erro = ""

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not titulo or not descricao:
            erro = "Preencha o título e a descrição da demanda."
        elif len(titulo) > 120:
            erro = "O título deve ter no máximo 120 caracteres."
        elif len(descricao) > 1000:
            erro = "A descrição deve ter no máximo 1000 caracteres."

        if erro:
            conteudo_erro = (
                '<section class="painel" role="alert">'
                f"<p>{escape(erro)}</p>"
                "</section>"
            )
            resposta = _formulario_demanda(conteudo_erro)
            return _pagina("Registrar demanda", resposta), 400

        with obter_conexao() as conexao:
            conexao.execute(
                """
                INSERT INTO demandas (titulo, descricao)
                VALUES (%s, %s)
                """,
                (titulo, descricao),
            )

        return redirect(url_for("rotas.consultar_demandas"))

    return _pagina("Registrar demanda", _formulario_demanda(""))


def _formulario_demanda(mensagem):
    return (
        "<h1>Registrar demanda</h1>"
        "<p>Preencha os campos para cadastrar uma solicitação.</p>"
        f"{mensagem}"
        '<section class="painel">'
        '<form class="formulario" method="post">'
        '<div class="campo">'
        '<label for="titulo">Título da demanda</label>'
        '<input id="titulo" name="titulo" maxlength="120" '
        'required autocomplete="off">'
        "</div>"
        '<div class="campo">'
        '<label for="descricao">Descrição</label>'
        '<textarea id="descricao" name="descricao" maxlength="1000" '
        'required></textarea>'
        "</div>"
        '<button type="submit">Salvar demanda</button>'
        "</form>"
        '<nav class="navegacao" aria-label="Navegação">'
        '<a href="/">Voltar ao início</a>'
        '<a href="/demandas">Consultar demandas</a>'
        "</nav>"
        "</section>"
    )


@rotas.route("/demandas/<int:id_demanda>/status", methods=["POST"])
def atualizar_status(id_demanda):
    novo_status = request.form.get("status", "").strip()

    if novo_status not in STATUS_PERMITIDOS:
        return (
            _pagina(
                "Status inválido",
                '<section class="painel" role="alert">'
                "<h1>Status inválido</h1>"
                "<p>Selecione um dos status disponíveis.</p>"
                '<a href="/demandas">Voltar às demandas</a>'
                "</section>",
            ),
            400,
        )

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
        return (
            _pagina(
                "Demanda não encontrada",
                '<section class="painel">'
                "<h1>Demanda não encontrada</h1>"
                '<a href="/demandas">Voltar às demandas</a>'
                "</section>",
            ),
            404,
        )

    return redirect(url_for("rotas.consultar_demandas"))


@rotas.route(
    "/demandas/<int:id_demanda>/atualizacoes",
    methods=["GET", "POST"],
)
def registrar_atualizacao(id_demanda):
    with obter_conexao() as conexao:
        demanda = conexao.execute(
            "SELECT id, titulo FROM demandas WHERE id = %s",
            (id_demanda,),
        ).fetchone()

    if demanda is None:
        return (
            _pagina(
                "Demanda não encontrada",
                '<section class="painel">'
                "<h1>Demanda não encontrada</h1>"
                '<a href="/demandas">Voltar às demandas</a>'
                "</section>",
            ),
            404,
        )

    if request.method == "POST":
        comentario = request.form.get("comentario", "").strip()

        if not comentario or len(comentario) > 1000:
            conteudo_erro = (
                '<section class="painel" role="alert">'
                "<p>Informe um comentário com até 1000 caracteres.</p>"
                "</section>"
            )
            return (
                _pagina(
                    "Registrar atualização",
                    _formulario_atualizacao(
                        demanda, conteudo_erro
                    ),
                ),
                400,
            )

        with obter_conexao() as conexao:
            conexao.execute(
                """
                INSERT INTO atualizacoes (demanda_id, comentario)
                VALUES (%s, %s)
                """,
                (id_demanda, comentario),
            )

        return redirect(url_for("rotas.consultar_demandas"))

    return _pagina(
        "Registrar atualização",
        _formulario_atualizacao(demanda, ""),
    )


def _formulario_atualizacao(demanda, mensagem):
    return (
        "<h1>Registrar atualização</h1>"
        '<section class="painel">'
        f"<p><strong>Demanda:</strong> {escape(demanda['titulo'])}</p>"
        f"{mensagem}"
        '<form class="formulario" method="post">'
        '<div class="campo">'
        '<label for="comentario">Comentário / Atualização</label>'
        '<textarea id="comentario" name="comentario" maxlength="1000" '
        'required aria-describedby="ajuda-comentario"></textarea>'
        '<p id="ajuda-comentario" class="texto-suave">'
        "Descreva o andamento da demanda, com até 1000 caracteres."
        "</p>"
        "</div>"
        '<button type="submit">Salvar atualização</button>'
        "</form>"
        '<nav class="navegacao" aria-label="Navegação">'
        '<a href="/demandas">Voltar às demandas</a>'
        '<a href="/">Voltar ao início</a>'
        "</nav>"
        "</section>"
    )
