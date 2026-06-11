import random
import time

from src.order import Ordem


class Simulador:
    """
    Classe responsavel por criar simulacoes de ordens
    para testar o livro de ofertas.
    """

    def gerar_ordem(self, id):
        """
        Gera uma unica ordem aleatoria.
        """

        tipo = random.choice(["C", "V"])
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
        Gera uma lista com varias ordens.
        """

        ordens = []

        for i in range(quantidade):

            ordem = self.gerar_ordem(i)

            ordens.append(ordem)

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



    def testar_carga(self, quantidades):
        """
        Executa simulacoes com diferentes quantidades
        de ordens.
        """

        resultados = {}


        for quantidade in quantidades:

            tempo = self.medir_tempo_execucao(
                lambda:
                self.gerar_ordens(quantidade)
            )


            resultados[quantidade] = tempo


        return resultados