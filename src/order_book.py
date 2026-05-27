from node import Node

class Transacao:
    """Representa uma negociação executada."""
    def __init__(self, id_compra, id_venda, preco, quantidade, timestamp):
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp

    def __str__(self):
        return f"Compra {self.id_compra} / Venda {self.id_venda} | Preço: {self.preco} | Qtd: {self.quantidade} | {self.timestamp}"

class HistoricoTransacoes:
    """
    Lista encadeada simples (ou dupla) que armazena transações em ordem cronológica.
    Mantém início, fim e tamanho.
    """
    def __init__(self):
        self.head = None   # primeira transação
        self.tail = None   # última transação
        self.size = 0

    def adicionar(self, transacao):
        """Insere uma nova transação no final do histórico."""
        novo_no = Node(transacao)
        if self.is_empty():
            self.head = novo_no
            self.tail = novo_no
        else:
            self.tail.next = novo_no
            novo_no.prev = self.tail   # se quiser duplamente encadeado; senão, remova o prev
            self.tail = novo_no
        self.size += 1

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size

    def imprimir(self):
        """Exibe todas as transações na ordem em que ocorreram."""
        if self.is_empty():
            print("Histórico vazio.")
            return
        current = self.head
        idx = 1
        while current:
            print(f"{idx}: {current.data}")
            current = current.next
            idx += 1

    # Opcional: método para limpar histórico
    def limpar(self):
        self.head = None
        self.tail = None
        self.size = 0