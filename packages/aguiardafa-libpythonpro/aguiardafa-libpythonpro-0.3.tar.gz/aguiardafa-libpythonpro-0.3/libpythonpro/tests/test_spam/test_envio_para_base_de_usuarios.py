import pytest

from libpythonpro.spam.enviador_de_email import Enviador
from libpythonpro.spam.main import EnviadorDeSpam
from libpythonpro.spam.models import Usuario

"""
Teste implementado utilizando injeção de dependências na criação do Mock
"""


class EnviadorMock(Enviador):
    def __init__(self):
        super().__init__()
        self.qtd_emails_enviados = 0
        self.parametros_de_envio = None

    def enviar(self, remetente, destinatario, assunto, corpo):
        self.parametros_de_envio = (remetente, destinatario, assunto, corpo)
        self.qtd_emails_enviados += 1


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='Diego', email='diego.fernandes.aguiar@gmail.com'),
            Usuario(nome='Aguiar', email='diego.fernandes.aguiar@gmail.com')
        ],
        [
            Usuario(nome='Diego', email='diego.fernandes.aguiar@gmail.com'),
        ]
    ]
)
def test_qtd_de_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    enviador = EnviadorMock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'diego.fernandes.aguiar@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    assert len(usuarios) == enviador.qtd_emails_enviados


def test_parametros_de_spam(sessao):
    usuario = Usuario(nome='Diego', email='diego.fernandes.aguiar@gmail.com')
    sessao.salvar(usuario)
    enviador = EnviadorMock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'dieguinho.uft@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    assert enviador.parametros_de_envio == (
        'dieguinho.uft@gmail.com',
        'diego.fernandes.aguiar@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
