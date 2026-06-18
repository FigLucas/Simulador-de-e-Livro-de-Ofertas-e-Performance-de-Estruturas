# Simulador de Livro de Ofertas

Projeto desenvolvido para a disciplina **SME0827 - Estruturas de Dados**.

<p align="center">
  <img width="900" alt="Arquitetura do Projeto" src="https://github.com/user-attachments/assets/c2df6cfc-b7f9-4843-bb22-7663926d7423" />
</p>

O projeto implementa um simulador de **livro de ofertas de compra e venda**. As ordens entram por uma fila, são inseridas em listas encadeadas ordenadas por prioridade de preço e tempo, podem gerar negociações quando há compatibilidade entre compra e venda, e as transações executadas ficam registradas em um histórico encadeado.

## Objetivo

Aplicar estruturas de dados lineares em um problema inspirado em sistemas de negociação, usando implementações próprias de:

* nó encadeado;
* fila encadeada;
* pilha encadeada;
* lista duplamente encadeada;
* histórico encadeado de transações.

## Regras do livro

Cada ordem possui:

* `id`: identificador único;
* `tipo`: `C` para compra ou `V` para venda;
* `preco`: preço limite;
* `quantidade`: quantidade ofertada;
* `timestamp`: horário de criação.

As compras são mantidas em ordem decrescente de preço, deixando a maior compra no início da lista. As vendas são mantidas em ordem crescente de preço, deixando a menor venda no início da lista.

Quando duas ordens têm o mesmo preço, a mais antiga tem prioridade, preservando FIFO dentro do mesmo nível de preço.

Uma transação ocorre quando:

```text
melhor_compra.preco >= melhor_venda.preco
```

A quantidade negociada é:

```text
min(melhor_compra.quantidade, melhor_venda.quantidade)
```

Ordens parcialmente executadas continuam no livro com a quantidade restante. Ordens totalmente executadas são removidas.

## Componentes principais

| Arquivo | Função |
| --- | --- |
| `src/node.py` | Define o nó usado pelas estruturas encadeadas. |
| `src/order.py` | Define a classe `Ordem` e valida tipo, preço e quantidade. |
| `src/queue.py` | Implementa a fila encadeada de entrada das ordens. |
| `src/stack.py` | Implementa a pilha usada no mecanismo de undo. |
| `src/doubly_linked_list.py` | Implementa a lista duplamente encadeada ordenada. |
| `src/order_book.py` | Implementa o livro, o histórico, o registro de IDs e o motor de negociação. |
| `src/simulator.py` | Gera ordens aleatórias e mede tempo de execução. |
| `main.py` | Executa uma demonstração do simulador. |

## Fluxo de execução

1. O motor recebe uma ordem e a coloca na fila de entrada.
2. A fila é processada em ordem FIFO.
3. Cada ordem é inserida no livro de ofertas correto: compras ou vendas.
4. O ID da ordem inserida é empilhado para permitir undo.
5. O motor verifica se a melhor compra cruza com a melhor venda.
6. Enquanto houver compatibilidade, as transações são executadas e registradas.
7. Ordens zeradas são removidas do início das listas.

O motor também mantém um registro encadeado de IDs já recebidos, evitando processar a mesma ordem mais de uma vez.

## Undo

O undo usa uma pilha de IDs inseridos no livro. Ao desfazer, o motor procura a última ordem que ainda está ativa e a remove.

Ordens já totalmente executadas não são restauradas. Nesses casos, o motor apenas desempilha o ID e continua procurando a ordem ativa anterior. Portanto, o undo cancela ordens ainda abertas, mas não desfaz transações já registradas.

## Simulador

A classe `Simulador`, em `src/simulator.py`, gera ordens aleatórias para demonstrações e testes de desempenho.

Ela possui:

* `gerar_ordem(id)`: cria uma ordem aleatória;
* `gerar_ordens(quantidade)`: cria uma `Fila` com várias ordens aleatórias;
* `medir_tempo_execucao(funcao)`: mede o tempo de execução de uma função.

## Como executar

No Windows:

```powershell
py main.py
```

Ou, se `python` estiver configurado no `PATH`:

```bash
python main.py
```

A execução principal demonstra inserção de ordens, processamento da fila, cruzamento de ofertas, match parcial, impressão do livro, undo e geração de ordens aleatórias.

## Relatório de performance

O notebook com a análise teórica e empírica está em:

```text
notebook/relatorio_performance.ipynb
```

Para executar o notebook, instale as dependências:

```bash
pip install -r requirements.txt
```

## Complexidade

Fila e pilha têm operações principais em tempo constante:

```text
O(1)
```

No livro de ofertas, a inserção ordenada, a busca por ID e a remoção por ID podem percorrer a lista:

```text
O(n)
```

Como o processamento completo executa essas operações para várias ordens, o custo acumulado pode se aproximar de:

```text
O(n²)
```

Esse comportamento é esperado principalmente quando muitas ordens são inseridas em listas já grandes ou quando ocorrem várias buscas e remoções.

## Organização

```text
.
|-- main.py
|-- README.md
|-- requirements.txt
|-- notebook/
|   `-- relatorio_performance.ipynb
|-- src/
    `-- __init__.py
    `-- doubly_linked_list.py
    `-- node.py
    `-- order.py
    `-- order_book.py

    `-- queue.py
    `-- simulator.py
    `-- stack.py
```
