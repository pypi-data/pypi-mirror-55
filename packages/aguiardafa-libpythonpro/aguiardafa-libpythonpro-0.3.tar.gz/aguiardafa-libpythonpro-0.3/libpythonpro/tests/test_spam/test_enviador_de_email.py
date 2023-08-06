import pytest

from libpythonpro.spam.enviador_de_email import Enviador, EmailInvalido


def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None


@pytest.mark.parametrize(
    'remetente',
    ['diego.fernandes.aguiar@gmail.com', 'dieguinho.uft@gmail.com']
)
def test_remetente(remetente):
    enviador = Enviador()

    resultado = enviador.enviar(
        remetente,
        'aguiardafa@decea.gov.br',
        'Assunto E-mail',
        'Corpo do E-mail'
    )
    assert remetente in resultado


@pytest.mark.parametrize(
    'remetente',
    ['', 'diego.gmail.com']
)
def test_remetente_invalido(remetente):
    enviador = Enviador()
    with pytest.raises(EmailInvalido):
        enviador.enviar(
            remetente,
            'aguiardafa@decea.gov.br',
            'Assunto E-mail',
            'Corpo do E-mail'
        )
