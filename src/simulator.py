import random
import time

from src.order import Ordem
from src.queue import Fila


class Simulador:
    """
    Classe responsavel por criar simulacoes de ordens
    para testar o livro de ofertas.
    """

    def gerar_ordem(self, id):
        """
        Gera uma unica ordem aleatoria.
        """

        if random.randint(0, 1) == 0:
            tipo = "C"
        else:
            tipo = "V"
        preco = round(random.uniform(10, 500), 2)
        quantidade = random.randint(1, 100)

        timestamp = time.time()

        return Ordem(
            id,
            tipo,
            preco,
            quantidade,
            timestamp
        )


    def gerar_ordens(self, quantidade):
        """
        Gera uma fila encadeada com varias ordens.
        """

        ordens = Fila()

        for i in range(quantidade):

            ordem = self.gerar_ordem(i)

            ordens.insere(ordem)

        return ordens



    def medir_tempo_execucao(self, funcao):
        """
        Mede o tempo necessario para executar
        uma determinada funcao.
        """

        inicio = time.time()

        funcao()

        fim = time.time()


        return fim - inicio

