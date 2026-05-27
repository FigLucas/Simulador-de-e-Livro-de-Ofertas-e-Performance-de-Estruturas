class Node:
    """Nó básico para listas encadeadas (dupla ou simples)."""
    def __init__(self, data):
        self.data = data      # Pode ser um objeto Order ou Transacao
        self.next = None
        self.prev = None