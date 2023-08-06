from libpythonpro.spam.models import Usuario


def test_salvar_usuario(sessao):
    usuario = Usuario(nome='Diego', email='diego.fernandes.aguiar@gmail.com')
    sessao.salvar(usuario)
    assert isinstance(usuario.id, int)


def test_listar_usuarios(sessao):
    usuarios = [
        Usuario(nome='Diego', email='diego.fernandes.aguiar@gmail.com'),
        Usuario(nome='Aguiar', email='diego.fernandes.aguiar@gmail.com')
    ]
    for usuario in usuarios:
        sessao.salvar(usuario)
    assert usuarios == sessao.listar()
