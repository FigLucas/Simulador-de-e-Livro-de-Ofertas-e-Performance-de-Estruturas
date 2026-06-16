import time

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
class MotorNegociacao:
    """Motor de negociação responsável pelo cruzamento de ordens (match), 
    gerenciamento da fila de entrada e controle de histórico para undo"""
    def __init__(self, fila_entrada, livro_ofertas, pilha_undo, verbose =True):
        self.fila = fila_entrada
        self.livro = livro_ofertas
        self.pilha = pilha_undo
        self.ids_utilizados = set()
        self.verbose = verbose
        
    def receber_nova_ordem(self, ordem):
        if ordem.id in self.ids_utilizados:
            print(f"Erro: A ordem com ID {ordem.id} já foi processada.")
            return
        self.fila.insere(ordem)
        self.ids_utilizados.add(ordem.id)
        if self.verbose:
            print(f"Ordem {ordem.id} adicionada com sucesso.")
            
    def processar_fila_para_o_livro(self):
        while not self.fila.estaVazia():
            ordem_atual = self.fila.remove()
            self.livro.inserir_ordem(ordem_atual)
            self.pilha.empilha(ordem_atual.id)
            if self.verbose:
                print(f"Ordem {ordem_atual.id} movida da fila para o Livro de Ofertas.")
        self.processar_match()

    def processar_match(self):
        if self.verbose:
            print("Procurando matches compatíveis no Livro de Ofertas...")
        while True:
            melhor_compra = self.livro.obter_melhor_compra()
            melhor_venda = self.livro.obter_melhor_venda()
            if melhor_compra is None or melhor_venda is None:
                break
            if melhor_compra.preco >= melhor_venda.preco:
                qtd_negociada = min (melhor_compra.quantidade, melhor_venda.quantidade)
                if qtd_negociada <= 0:
                    if melhor_compra.quantidade <= 0: self.livro.remover_ordem_por_id(melhor_compra.id)
                    if melhor_venda.quantidade <= 0: self.livro.remover_ordem_por_id(melhor_venda.id)
                    continue
                if melhor_compra.timestamp < melhor_venda.timestamp:
                    preco_fechamento = melhor_compra.preco
                else:
                    preco_fechamento = melhor_venda.preco
                transacao = Transacao(
                    melhor_compra.id,
                    melhor_venda.id,
                    preco_fechamento,
                    qtd_negociada,
                    time.time()
                )
                self.livro.historico.adicionar(transacao)
                melhor_compra.quantidade -= qtd_negociada
                melhor_venda.quantidade -= qtd_negociada
                if self.verbose:
                    print(f"Transação efetuada! {qtd_negociada} unidades fechadas a R$ {preco_fechamento:.2f}")
                if melhor_compra.quantidade == 0:
                    self.livro.remover_ordem_por_id(melhor_compra.id)
                if melhor_venda.quantidade == 0:
                    self.livro.remover_ordem_por_id(melhor_venda.id)
            else:
                break

    def desfazer_ultima_insercao(self):
        if self.verbose: 
            print("\n Executando comando Undo (Desfazer)...")
        if self.pilha.estaVazia():
            if self.verbose: 
                print("Nada para desfazer. A pilha está vazia.")
            return
        while not self.pilha.estaVazia():
            id_para_cancelar = self.pilha.desempilha()      
            if self.livro.ordem_existe(id_para_cancelar):
                self.livro.remover_ordem_por_id(id_para_cancelar)
                if self.verbose: print(f"Sucesso: Ordem {id_para_cancelar} cancelada e removida do livro.")
                break 
            else:
                if self.verbose: print(f"Ordem {id_para_cancelar} já foi totalmente executada.")
