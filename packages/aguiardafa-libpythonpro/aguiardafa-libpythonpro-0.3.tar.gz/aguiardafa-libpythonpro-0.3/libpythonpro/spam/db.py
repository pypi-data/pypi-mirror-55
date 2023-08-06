from time import sleep


class Sessao:
    contador = 0
    usuarios = []

    def salvar(self, usuario):
        Sessao.contador += 1
        usuario.id = Sessao.contador
        self.usuarios.append(usuario)

    def listar(self):
        return self.usuarios

    def roll_back(self):
        self.usuarios.clear()
        Sessao.contador = 0

    def fechar(self):
        pass


class Conexao:

    def __init__(self):
        """
            Emulando a demora da abertura de uma conexão
            a fim de demonstrar a necessidade de ampliação do escopo de fixture
            O escopo padrão é por função
            Porém ampliaremos para módulo
            De modo que a criação da Conexão seja realizada uma vez pra cada módulo que a usa
        """
        sleep(10)

    def gerar_sessao(self):
        return Sessao()

    def fechar(self):
        pass
