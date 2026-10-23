from flask import Flask

from .rotas import rotas


def criar_aplicacao():
    aplicacao = Flask(__name__)
    aplicacao.register_blueprint(rotas)

    return aplicacao
