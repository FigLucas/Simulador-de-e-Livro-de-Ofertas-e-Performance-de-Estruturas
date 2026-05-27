from node import Node

class DoublyLinkedList:
    """
    Lista duplamente encadeada que mantém a ordem de inserção baseada em um critério.
    Atributos:
        head (Node): primeiro nó
        tail (Node): último nó
        size (int): quantidade de nós
        order_type (str): 'buy' (decrescente por preço) ou 'sell' (crescente por preço)
    """
    def __init__(self, order_type='buy'):
        self.head = None
        self.tail = None
        self.size = 0
        self.order_type = order_type   # 'buy' ou 'sell'

    # ---------- Métodos básicos de consulta e impressão ----------
    def is_empty(self):
        return self.size == 0

    def get_first(self):
        """Retorna o primeiro nó (melhor oferta)."""
        return self.head

    def get_last(self):
        return self.tail

    def print_list(self):
        """Exibe todos os elementos na ordem da lista."""
        current = self.head
        elements = []
        while current:
            order = current.data
            elements.append(f"ID:{order.id} Preço:{order.preco} Qtd:{order.quantidade}")
            current = current.next
        print(f"Lista ({self.order_type}): " + " -> ".join(elements))

    # ---------- Método auxiliar para comparar ordem ----------
    def _should_come_before(self, new_order, current_order):
        """
        Decide se new_order deve ser inserido ANTES de current_order.
        Regras:
            - Compra (buy): ordem decrescente de preço (maior preço primeiro).
              Se preços iguais, o mais antigo (timestamp menor) fica antes.
            - Venda (sell): ordem crescente de preço (menor preço primeiro).
              Se preços iguais, o mais antigo fica antes.
        """
        if self.order_type == 'buy':
            # Queremos maior preço primeiro. Se preço maior, vem antes.
            if new_order.preco > current_order.preco:
                return True
            if new_order.preco < current_order.preco:
                return False
            # Preços iguais: mais antigo (timestamp menor) primeiro
            return new_order.timestamp < current_order.timestamp
        else:  # sell
            # Menor preço primeiro
            if new_order.preco < current_order.preco:
                return True
            if new_order.preco > current_order.preco:
                return False
            return new_order.timestamp < current_order.timestamp

    # ---------- Inserção ordenada (posição correta) ----------
    def insert_ordered(self, new_node):
        """
        Insere o nó na posição correta baseada nas regras de ordenação.
        Percorre a lista (O(n)) e insere no início, meio ou fim.
        """
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            current = self.head
            # Encontra a posição onde new_node deve ser inserido
            while current and not self._should_come_before(new_node.data, current.data):
                current = current.next

            if current is None:
                # Insere no final
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            elif current.prev is None:
                # Insere no início
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
            else:
                # Insere no meio
                prev_node = current.prev
                prev_node.next = new_node
                new_node.prev = prev_node
                new_node.next = current
                current.prev = new_node
        self.size += 1

    # ---------- Busca por ID ----------
    def find_by_id(self, order_id):
        """Retorna o nó que contém a ordem com o ID informado, ou None."""
        current = self.head
        while current:
            if current.data.id == order_id:
                return current
            current = current.next
        return None

    # ---------- Remoção do primeiro nó (melhor oferta) ----------
    def remove_first(self):
        """Remove e retorna o primeiro nó (head). Retorna None se vazia."""
        if self.is_empty():
            return None
        removed = self.head
        if self.head == self.tail:  # apenas um elemento
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return removed

    # ---------- Remoção por ID ----------
    def remove_by_id(self, order_id):
        """Remove o nó que contém o ID informado. Retorna o nó removido ou None."""
        node_to_remove = self.find_by_id(order_id)
        if node_to_remove is None:
            return None

        # Ajusta ponteiros
        prev_node = node_to_remove.prev
        next_node = node_to_remove.next

        if prev_node:
            prev_node.next = next_node
        else:
            # remove o head
            self.head = next_node

        if next_node:
            next_node.prev = prev_node
        else:
            # remove o tail
            self.tail = prev_node

        self.size -= 1
        node_to_remove.prev = None
        node_to_remove.next = None
        return node_to_remove