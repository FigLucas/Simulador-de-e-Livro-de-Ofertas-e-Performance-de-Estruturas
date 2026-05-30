class Ordem:
    """
    Classe para representar uma ordem de compra ou venda.
    """
    def __init__(self, id: int, tipo: str, preco: float, quantidade: int, timestamp):
        if tipo not in ("C", "V"):
            raise Exception("Tipo de ordem invalido! Deve ser C para compra ou V para venda.")
        if preco <= 0:
            raise Exception("Preco invalido! Deve ser maior que zero.")
        if quantidade <= 0:
            raise Exception("Quantidade invalida! Deve ser maior que zero.")

        self.id = id
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp

    def __str__(self):
        return (
            f"Ordem(id={self.id}, tipo={self.tipo}, "
            f"preco={self.preco:.2f}, qtde={self.quantidade}, "
            f"ts={self.timestamp})"
        )

    def eCompra(self):
        return self.tipo == "C"

    def eVenda(self):
        return self.tipo == "V"

    def reduzQuantidade(self, qtde: int):
        if qtde < 0:
            raise Exception("Quantidade a reduzir invalida! Deve ser maior ou igual a zero.")
        if qtde > self.quantidade:
            raise Exception("Quantidade a reduzir invalida! Excede a quantidade disponivel.")
        self.quantidade -= qtde

    def estaExecutada(self):
        return self.quantidade <= 0