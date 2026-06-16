from .node import Node

class Fila:
    """
    Classe para a fila encadeada (FIFO) usada para armazenar ordens antes do processamento.
    """

    def __init__(self):
        self.inicioFila = None
        self.fimFila = None
        self.tamanho = 0

    def __str__(self):
        saida = ""
        atual = self.inicioFila
        while atual is not None:
            saida += str(atual.data) + "->"
            atual = atual.next
        return saida

    def __iter__(self):
        atual = self.inicioFila
        while atual is not None:
            yield atual.data
            atual = atual.next

    def veTamanho(self):
        return self.tamanho

    def estaVazia(self):
        return self.tamanho == 0

    def inicio(self):
        if self.estaVazia():
            raise Exception("A fila esta vazia!")
        return self.inicioFila.data

    def fim(self):
        if self.estaVazia():
            raise Exception("A fila esta vazia!")
        return self.fimFila.data

    def insere(self, valor):
        novo = Node(valor)
        if self.estaVazia():
            self.inicioFila = novo
            self.fimFila = novo
        else:
            self.fimFila.next = novo
            self.fimFila = novo
        self.tamanho += 1

    def remove(self):
        if self.estaVazia():
            raise Exception("A fila esta vazia: nao é possivel remover elementos!")

        noRemovido = self.inicioFila
        valor = noRemovido.data
        self.inicioFila = self.inicioFila.next

        if self.inicioFila is None:
            self.fimFila = None

        noRemovido.next = None
        self.tamanho -= 1
        return valor
