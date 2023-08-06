from unittest.mock import Mock

import pytest

from libpythonpro import githubapi


@pytest.fixture
def avatar_url(mocker):
    """
    Realizando setup utilizando o plugin pytest-mock
    para isolado uso do import de forma simplificada
    onde ele automaticamente retorna o import ao estado original após o teste
    """
    # setup
    url_esperada = 'https://avatars0.githubusercontent.com/u/16319889?v=4'

    resp_mock = Mock()
    resp_mock.json.return_value = {
        'avatar_url': url_esperada
    }
    get_mock = mocker.patch('libpythonpro.githubapi.requests.get')
    get_mock.return_value = resp_mock

    return url_esperada


def test_buscar_avatar(avatar_url):
    """
    Exemplo de Teste em Python utilizando o framework Pytest
    Assim NÃO sendo necessário importação

    Utilizando ainda a lib Mock do unittest para isolar o teste em um teste unitário
    simulando o comportamento da API para testar simplesmente o método buscar
    ou seja, o teste independe da integração com a API
    """
    usuario = 'aguiardafa'
    url_esperada = avatar_url

    url_obtida = githubapi.buscar_avatar(usuario)

    assert url_esperada == url_obtida


def test_busca_avatar_integracao():
    usuario = 'renzon'
    url_esperada = "https://avatars3.githubusercontent.com/u/3457115?v=4"

    url_obtida = githubapi.buscar_avatar(usuario)

    assert url_esperada == url_obtida
