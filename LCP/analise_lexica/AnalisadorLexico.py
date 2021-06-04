from Token import Token
from Erro import Erro

class AnalisadorLexico:

    def __init__(self):
        #FLAGS PARA CONTROLE
        self.__COMENTARIO = False
        self.__IDENTIFICADOR = False
        self.__DOIS_PONTOS = False
        self.__TEXTO = False
        self.__DIFERENTE = False
        self.__INDENTIFICADOR = False
        self.__NUMERO = False
        self.__LOGICO = False
        self.__PALAVRA = False
        self.__LOGICOS = ['Sim', 'Nao']
        self.__RESERVADOS = [
            'Funcao',
            'Logica',
            'Texto',
            'Numero',
            'Logico',
            'se',
            'se nao',
            'se nao se',
            'enquanto',
            'retorna'
        ]
        
    #REALIZA A ANALISE LEXICA
    def analisar(self, programa):
        #VARIAVEIS
        tk = {}
        tokens = []
        erros = []
        anterior = ''
        palavra = ''
        primeira_letra = ''
        linha = 1
        indice = -1
        indice_palavra = -1
        
        #PARA CADA CARACTÉR NA ENTRADA
        for c in programa:
            indice += 1
            
            #DA A MAIOR PRIORIDADE PARA O CASO DE COMENTÁRIO
            #VERIFICANDO A EXISTÊNCIA DO '-' E GUARDANDO PARA A PRÓXIMA EXECUÇÃO
            #SE O PROXIMO CARACTER TAMBÉM FOR UM '-' O ADICIONA NO TOKEN ATÉ ENCONTRAR UM '\n'
            if c == '-':
                if not self.__COMENTARIO:
                    if anterior == '':
                        anterior = c
                        continue
                    if anterior == '-':
                        self.__COMENTARIO = True
                        anterior = ''
                        tk = Token('comentario', '--', linha, indice - 1)
                        continue
            elif self.__COMENTARIO:
                if c == '\n':
                    self.__COMENTARIO = False
                    tokens.append(tk.toDict())
                    tk = {}
                else:
                    tk.addTexto(c)
                    continue
            #A SEGUNDA MAIOR PRIORIDADE É PARA STRING
            #ANALISA TAMBÉM OS CARACTERES '#' GUARDANDO-OS PARA VERIFICAR
            #NA PROXIMA EXECUÇÃO SE ERA UM ESCAPE OU NÃO
            if(c == '\'' and not self.__TEXTO):
                self.__TEXTO = True
                tk = Token('texto', '\'', linha, indice)
                continue
            if self.__TEXTO:
                tk.addTexto(c)
                if anterior == '#':
                    anterior = ''
                    continue
                if c == '\'':
                    self.__TEXTO = False
                    tokens.append(tk.toDict())
                    tk = {}
                elif c == '#':
                    anterior = '#'
                continue
            
            #GUARDA AS PALAVRAS ENCONTRADAS PARA ANALISAR CASOS DE RESERVADOS, LOGICOS E IDENTICADORES
            #ACUMULA CARACTERES ENQUANTO FOR LETRA OU ESPAÇO EM BRANCO
            if c.isalpha() and not self.__PALAVRA:
                self.__PALAVRA = True
                palavra += c
                indice_palavra = indice
                primeira_letra = c
                if not self.__DOIS_PONTOS and not self.__DIFERENTE:
                    continue
            elif self.__PALAVRA :
                #AO FINALIZAR A PALAVRA VERIFICA SE ELA ESTÁ RESERVADA
                if not c.isalpha() and c != " ":
                    self.__PALAVRA = False
                    palavra = palavra.strip()
                    if palavra in self.__RESERVADOS:
                        tokens.append(Token('reservado', palavra, linha, indice_palavra).toDict())
                    #CASO O CONTRÁRIO REALIZA UM SPLIT C/ ESPAÇO PARA ANALISAR CADA PALAVRA SEPARADAMENTE
                    #POSSIBILITA A IDENTIFICAÇÃO DE 'SE', 'SE NÃO' E 'SE NÃO SE' NOS RESERVADOS
                    else:
                        for p in palavra.split(' '):
                            if p in self.__RESERVADOS:
                                tokens.append(Token('reservado', p, linha, indice_palavra).toDict())
                            elif p in self.__LOGICOS:
                                tokens.append(Token('logico', p, linha, indice_palavra).toDict())
                            elif primeira_letra.islower():
                                tokens.append(Token('identificador', p, linha, indice_palavra).toDict())
                            else:
                                tokens.append(Token('desconhecido', p, linha, indice_palavra).toDict())
                                erros.append(Erro('simbolo, ' + p + ', desconhecido', linha, indice_palavra).toDict())
                            indice_palavra += (1 + len(p))
                    palavra = ''
                else:
                    palavra += c
                    continue

            #IDENTIFICA NUMEROS
            if c.isnumeric() and not self.__NUMERO:
                self.__NUMERO = True
                tk = Token('numero', c, linha, indice)
                continue
            if self.__NUMERO:
                if not c.isnumeric():
                    self.__NUMERO = False
                    tokens.append(tk.toDict())
                    tk = {}
                else:
                    tk.addTexto(c)
                    continue
            
            #AO ENCONTRAR UMA EXCLAMAÇÃO O GUARDA PARA ANALISAR NA PROXIMA ITERAÇÃO SE É '!='
            if(c == '!'):
                anterior = '!'
                self.__DIFERENTE = True
                continue
            if self.__DIFERENTE:
                if c == '=':
                    tokens.append(Token('operador-diferente', '!=', linha, indice - 1).toDict())
                    self.__DIFERENTE = False
                    anterior = ''
                    continue
            
            #ANALISE DE CASOS SIMPLES
            if c == '(':
                tokens.append(Token('abre-parenteses', '(', linha, indice).toDict())
                continue
            if c == ')':
                tokens.append(Token('fecha-parenteses', ')', linha, indice).toDict())
                continue
            if c == '{':
                tokens.append(Token('abre-chaves', '{', linha, indice).toDict())
                continue
            if c == '}':
                tokens.append(Token('fecha-chaves', '}', linha, indice).toDict())
                continue
            if c == ',':
                tokens.append(Token('virgula', ',', linha, indice).toDict())
                continue
            if c == '=':
                tokens.append(Token('operador-igual', '=', linha, indice).toDict())
                continue
            if c == '<':
                tokens.append(Token('operador-menor', '<', linha, indice).toDict())
                continue
            if c == '>':
                tokens.append(Token('operador-maior', '>', linha, indice).toDict())
                continue
            if c == '+':
                tokens.append(Token('operador-mais', '+', linha, indice).toDict())
                continue
            
            #GUARDA A PRIMEIRA OCORRÊNCIA DE ":" PARA ANALISAR NA PROXIMA ITERAÇÃO SE É UMA ATRIBUIÇÃO OU DOIS-PONTOS
            if c == ':' and anterior == '':
                self.__DOIS_PONTOS = True
                anterior = c
                continue	
            if self.__DOIS_PONTOS:
                anterior = ''
                self.__DOIS_PONTOS = False
                if c == ':':				
                    tokens.append(Token('atribuicao', '::', linha, indice - 1).toDict())
                    continue
                tokens.append(Token('dois-pontos', ':', linha, indice - 1).toDict())
                continue
            
            #ANALISA QUEBRA DE LINHA
            if c == '\n':
                tokens.append(Token('quebra-linha', '\n', linha, indice).toDict())
                linha += 1
                indice = -1
                continue
            
            #SE NÃO ENTROU EM NENHUMA REGRA, CONSIDERA UM DESCONHECIDO, LANCANDO UM ERRO
            if c != " ":
                tokens.append(Token('desconhecido', c, linha, indice).toDict())
                erros.append(Erro('simbolo, ' + c + ', desconhecido', linha, indice).toDict())

        return tokens, erros
