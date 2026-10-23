from flask import Flask


def criar_aplicacao():
    aplicacao = Flask(__name__)
    return aplicacao
