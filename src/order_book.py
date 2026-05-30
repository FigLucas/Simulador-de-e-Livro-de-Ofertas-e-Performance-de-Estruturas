from .node import Node
from .doubly_linked_list import DoublyLinkedList

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
    """Lista encadeada para armazenar transações em ordem cronológica."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def adicionar(self, transacao):
        novo_no = Node(transacao)
        if self.is_empty():
            self.head = novo_no
            self.tail = novo_no
        else:
            self.tail.next = novo_no
            novo_no.prev = self.tail
            self.tail = novo_no
        self.size += 1

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size

    def imprimir(self):
        if self.is_empty():
            print("Histórico vazio.")
            return
        current = self.head
        idx = 1
        while current:
            print(f"{idx}: {current.data}")
            current = current.next
            idx += 1

    def limpar(self):
        self.head = None
        self.tail = None
        self.size = 0

class LivroOfertas:
    """
    Livro de ofertas que gerencia ordens de compra e venda.
    Utiliza apenas listas duplamente encadeadas ordenadas (sem mapas auxiliares).
    """
    def __init__(self):
        self.compras = DoublyLinkedList(order_type='buy')
        self.vendas = DoublyLinkedList(order_type='sell')
        self.historico = HistoricoTransacoes()

    def inserir_ordem(self, order):
        if self.ordem_existe(order.id):
            print(f"Erro: Ordem com ID {order.id} já existe.")
            return False
        novo_no = Node(order)
        if order.tipo == 'C':
            self.compras.insert_ordered(novo_no)
        elif order.tipo == 'V':
            self.vendas.insert_ordered(novo_no)
        else:
            print(f"Erro: Tipo '{order.tipo}' inválido. Use 'C' ou 'V'.")
            return False
        return True

    def remover_ordem_por_id(self, order_id):
        if self.compras.remove_by_id(order_id):
            return True
        if self.vendas.remove_by_id(order_id):
            return True
        return False

    def obter_melhor_compra(self):
        if self.compras.is_empty():
            return None
        return self.compras.get_first().data

    def obter_melhor_venda(self):
        if self.vendas.is_empty():
            return None
        return self.vendas.get_first().data

    def ordem_existe(self, order_id):
        return (self.compras.find_by_id(order_id) is not None) or (self.vendas.find_by_id(order_id) is not None)

    def imprimir_livro(self):
        print("\n===== LIVRO DE OFERTAS =====")
        print("--- COMPRAS (maior preço primeiro) ---")
        self.compras.print_list()
        print("--- VENDAS (menor preço primeiro) ---")
        self.vendas.print_list()
        print("--- HISTÓRICO DE TRANSAÇÕES ---")
        self.historico.imprimir()
        print("=============================\n")

    def total_ordens(self):
        return self.compras.size + self.vendas.size