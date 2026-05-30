from .node import Node

class Pilha:
    """
    Classe para pilha encadeada para desfazer a última inserção realizada.
    """

    def __init__(self):
        self.topoPilha = None
        self.tamanho = 0

    def __str__(self):
        saida = ""
        atual = self.topoPilha
        while atual is not None:
            saida += str(atual.data) + "->"
            atual = atual.next
        return saida

    def veTamanho(self):
        return self.tamanho

    def estaVazia(self):
        return self.tamanho == 0

    def topo(self):
        if self.estaVazia():
            raise Exception("A pilha esta vazia!")
        return self.topoPilha.data

    def existeValor(self, valor):
        atual = self.topoPilha
        while atual is not None:
            if atual.data == valor:
                return True
            atual = atual.next
        return False

    def empilha(self, valor):
        novo = Node(valor)
        novo.next = self.topoPilha
        self.topoPilha = novo
        self.tamanho += 1

    def desempilha(self):
        if self.estaVazia():
            raise Exception("A pilha esta vazia: nao e possivel desempilhar!")

        noRemovido = self.topoPilha
        valor = noRemovido.data
        self.topoPilha = self.topoPilha.next
        noRemovido.next = None
        self.tamanho -= 1
        return valor