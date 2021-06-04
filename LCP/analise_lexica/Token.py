class Token:

    def __init__(self, grupo, texto, linha, indice):
        self.grupo = str(grupo)
        self.texto = str(texto)
        self.local = {
            "linha": int(linha),
            "indice": int(indice)
        }

    def addTexto(self, char):
        self.texto += str(char)

    def toDict(self):
        return self.__dict__