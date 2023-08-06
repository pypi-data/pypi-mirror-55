import pytest

from libpythonpro.spam.db import Conexao


@pytest.fixture(scope='module')
def conexao():
    # setup
    conexao_obj = Conexao()
    yield conexao_obj
    # tear down
    conexao_obj.fechar()


@pytest.fixture
def sessao(conexao):
    # setup
    sessao_obj = conexao.gerar_sessao()
    yield sessao_obj
    # tear down
    sessao_obj.roll_back()
    sessao_obj.fechar()
