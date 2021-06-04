from p1_inputs import *


def main():
    
    variaveis = input_variaveis()
    alfabeto = input_alfabeto()
    variavel_inicial = input_variavel_inicial(variaveis)
    regras = input_regras(variaveis, alfabeto)
    sequencia = input_sequencia(regras, variavel_inicial)
    
    palavra = variavel_inicial
    for sq in sequencia:
        sq = int(sq)
        key = list(regras[sq].keys())[0]
        palavra = palavra.replace(key, regras[sq][key],1)

    sucesso = True
    for char in list(palavra):
        if(not char in alfabeto):
            sucesso = False
            break
    
    if(sucesso):
        print("A palavra foi formada corretamente!")
    else:
        print("A palavra não foi formada corretamente!")

    print("Palavra: " + palavra + "\n")
    

if __name__ == "__main__":
    main()