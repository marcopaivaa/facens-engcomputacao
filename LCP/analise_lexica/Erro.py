class Erro:

    def __init__(self, texto, linha, indice):
        self.texto = str(texto)
        self.local = {
            "linha": int(linha),
            "indice": int(indice)
        }

    def addTexto(self, char):
        self.texto += str(char)

    def toDict(self):
        return self.__dict__