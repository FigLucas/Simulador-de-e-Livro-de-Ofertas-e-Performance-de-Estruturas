import random
import time
from src.order import Ordem
from src.order_book import LivroOfertas, MotorNegociacao
from src.queue import Fila
from src.simulator import Simulador
from src.stack import Pilha


def demonstrar_ordens_aleatorias(quantidade=10):
    print("\n--- Demonstracao com ordens aleatorias do Simulador ---")

    random.seed(42)
    simulador = Simulador()
    ordens = simulador.gerar_ordens(quantidade)

    fila = Fila()
    livro = LivroOfertas()
    pilha = Pilha()
    motor = MotorNegociacao(fila, livro, pilha, verbose=False)

    for ordem in ordens:
        motor.receber_nova_ordem(ordem)

    motor.processar_fila_para_o_livro()

    print(f"\nForam geradas e processadas {quantidade} ordens aleatorias.")
    print("Estado final do livro gerado pelo Simulador:")
    livro.imprimir_livro()


def main():
    print("--- Simulador de Livro de Ofertas ---")
    
    # Inicializa as estruturas do projeto
    fila = Fila()
    livro = LivroOfertas()
    pilha = Pilha()
    
    # Instancia o motor de negociacao
    motor = MotorNegociacao(fila, livro, pilha, verbose=True)
    
    print("\nInserindo ordens de teste na fila...")
    
    # Ordem 1: Compra
    o1 = Ordem(id=1, tipo='C', preco=100.0, quantidade=50, timestamp=time.time())
    motor.receber_nova_ordem(o1)
    time.sleep(0.02) 
    
    # Ordem 2: Venda (deve gerar match parcial com a ordem 1)
    o2 = Ordem(id=2, tipo='V', preco=90.0, quantidade=30, timestamp=time.time())
    motor.receber_nova_ordem(o2)
    time.sleep(0.02)
    
    # Ordem 3: Venda que vai ficar flutuando no livro
    o3 = Ordem(id=3, tipo='V', preco=110.0, quantidade=15, timestamp=time.time())
    motor.receber_nova_ordem(o3)
    time.sleep(0.02)
    
    # Ordem 4: Compra que vai ficar flutuando no livro
    o4 = Ordem(id=4, tipo='C', preco=85.0, quantidade=10, timestamp=time.time())
    motor.receber_nova_ordem(o4)
    
    print("\nProcessando a fila e executando os cruzamentos...")
    motor.processar_fila_para_o_livro()
    
    print("\nEstado do livro apos o processamento:")
    livro.imprimir_livro()
    
    print("\nTestando a funcao de desfazer (Undo)...")
    motor.desfazer_ultima_insercao()
    
    print("\nEstado do livro apos o Undo:")
    livro.imprimir_livro()

    demonstrar_ordens_aleatorias()

if __name__ == "__main__":
    main()
