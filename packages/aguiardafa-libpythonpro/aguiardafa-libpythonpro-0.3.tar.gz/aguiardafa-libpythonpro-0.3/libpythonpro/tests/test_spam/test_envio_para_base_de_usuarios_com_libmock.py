from unittest.mock import Mock

import pytest

from libpythonpro.spam.main import EnviadorDeSpam
from libpythonpro.spam.models import Usuario

"""
Teste implementado utilizando a lib Mock do Módulo unittest
"""


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
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'diego.fernandes.aguiar@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    assert len(usuarios) == enviador.enviar.call_count


def test_parametros_de_spam(sessao):
    usuario = Usuario(nome='Diego', email='diego.fernandes.aguiar@gmail.com')
    sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'dieguinho.uft@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    enviador.enviar.assert_called_once_with(
        'dieguinho.uft@gmail.com',
        'diego.fernandes.aguiar@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
