from functions import *

def input_sequencia(regras, variavel_inicial):
    print_regras(regras)
    while(True):
        loop = False
        sequencia = input("Digite a chave (#) da sequencia de regras separadas por espaco: ")
        if(sequencia.strip() == ""):
            print("Escolha pelo menos uma regra!")
            continue
        sequencia = sequencia.split()
        if(list(regras[int(sequencia[0])].keys())[0] != variavel_inicial):
            print("A sequencia deve iniciar com a variavel inicial!")
            continue
        for var in sequencia:
            var = int(var)
            if(var < 0 or var > len(regras) - 1):
                print("Sequencia invalida!")
                loop = True
                break
        if(not loop):
            return sequencia

def print_regras(regras):
    cls()
    print("\n")
    for regra in regras:
        print("Regra #" + str(regras.index(regra)) + ": " + str(regra))
    print("\n")

def input_regras(variaveis, alfabeto):
    regras = []
    while(True):
        loop = False
        regra = input("Digite uma regra separada por espaco (predecessor sucessor) ou 0 para continuar: ")
        if(regra == "0"):
            return regras
        regra = regra.split(" ")
        if(len(regra) != 2):
                print("Uma regra deve conter apenas dois parametros: predecessor e sucessor!")
                loop = True
                continue
        for var in regra:
            for char in list(var):
                if(not (char in variaveis or char in alfabeto)):
                    print("Cada caracter na regra deve pertencer as variaveis ou ao alfabeto!")
                    loop = True
                    break
            if(loop):
                break
        if(not loop):
            regras.append({
                regra[0]: regra[1]
            })

def input_variavel_inicial(variaveis):
    while(True):
        loop = False
        variavel_inicial = input("Digite a variavel inicial: ")
        if(not variavel_inicial in variaveis):
            print("A variavel inicial devem estar inclusa no conjunto de variaveis!")
            loop = True
        if(not loop):
            return variavel_inicial

def input_alfabeto():
    while(True):
        loop = False
        alfabeto = input("Digite os alfabeto separados por espaco: ")
        alfabeto = alfabeto.split(" ")
        for var in alfabeto:
            if(var.lower() != var):
                print("O alfabeto deve conter apenas letras minusculas ou simbolos/numeros!")
                loop = True
                break
        if(not loop):
            return alfabeto

def input_variaveis():
    while(True):
        loop = False
        variaveis = input("Digite as variaveis separadas por espaco: ")
        variaveis = variaveis.split(" ")
        for var in variaveis:
            if(var.upper() != var or var.isnumeric()):
                print("As variaveis devem conter apenas letras maiusculas!")
                loop = True
                break
        if(not loop):
            return variaveis