class MyStack:

    def __init__(self, m):
        self.topo = 0
        self.maximo = m
        self.elementos = []

    # Testando se a pilha está cheia
    def cheia(self):
        return self.topo == self.maximo

    # Empilhando elementos
    def push(self, x):
        if self.cheia():
            return False
        self.elementos.append(x)
        self.topo += 1

    # Verificando se a Pilha está vazia
    def vazia(self):
        return self.topo == 0

    # Desempilhando elementos
    def pop(self):
        if self.vazia():
            return False
        self.topo -= 1
        return self.elementos[self.topo]

    # Desempilhando elementos
    def top(self):
        if self.vazia():
            return False
        return self.elementos[self.topo-1]
