from structures.myQueue import MyQueue
from structures.myStack import MyStack
from structures.myNode import MyNode
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

STATE = -1
V_EMPTY = '#'


class Automata:

    def __init__(self):
        self.nodes = []
        self.init = None
        self.ends = []
        self.alphabet = []

    def createAutomata(self, regex):
        self.nodes = []
        regex = "(A|B)*.(C.D.E*)+" if regex == "-t" else regex
        prefix = self.toPrefix(regex)
        print("\nInfixa: " + regex)
        print("Prefixa: " + prefix)
        self.validateExpression(prefix)
        queue = self.enqueueStringChar(prefix)
        node = self.automata(queue)
        node.init = True
        self.init = node
        node.last.end = True
        self.ends = node.last
        return node

    def toPrefix(self, expr):
        expression = MyQueue()
        operator = MyStack(len(expr))
        prefixa = ""
        i = 0
        while(i < len(expr)):
            if ((expr[i] >= 'A' and expr[i] <= 'Z') or (expr[i] >= 'a' and expr[i] <= 'z')):
                self.alphabet.append(expr[i])
                prefixa += expr[i]
            elif (expr[i] == '*' or expr[i] == '+'):
                aux = prefixa[-1]
                prefixa = prefixa[:-1]
                prefixa += expr[i]
                prefixa += aux
            elif (expr[i] == '.' or expr[i] == '|'):
                operator.push(expr[i])
            elif (expr[i] == '('):
                if(i > 0 and expr[i-1] != '.' and expr[i-1] != '|'):
                    operator.push('.')
                j = i
                cont = 1
                while(cont >= 1):
                    j = j+1
                    if(expr[j] == '('):
                        cont = cont+1
                    elif(expr[j] == ')'):
                        cont = cont-1
                aux = self.toPrefix(expr[i+1:j])
                i = j
                if(i < len(expr) - 1 and (expr[i+1] == '*' or expr[i+1] == '+')):
                    aux = expr[i+1] + aux
                    i = i+1
                prefixa += aux
            i = i+1
        while(not operator.vazia()):
            prefixa = operator.pop() + prefixa
            if(operator.vazia()):
                expression.enqueue(prefixa)
                prefixa = ""
        while(len(prefixa) > 0):
            expression.enqueue(prefixa)
            prefixa = ""
        while (expression.size() > 0):
            prefixa += expression.dequeue()
        return prefixa

    def enqueueStringChar(self, str):
        queue = MyQueue()
        for char in list(str):
            queue.enqueue(char)
        return queue

    def validateExpression(self, prefix):
        alpha = 0
        op = 0
        for char in list(prefix):
            if((char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')):
                alpha += 1
            else:
                op += 1
        if(op < alpha - 1):
            raise Exception("Error! Verify the regex expression.")

    def automata(self, queue):
        v1 = queue.dequeue()

        if((v1 >= 'a' and v1 <= 'z') or (v1 >= 'A' and v1 <= 'Z')):
            return self.createNode(v1)
        else:
            n1 = self.automata(queue)

        if(v1 == "|" or v1 == "."):
            if(queue.size() == 0):
                return n1
            else:
                n2 = self.automata(queue)
    
        if(v1 == "|"):
            n = self.createOr(n1, n2)
        elif(v1 == "."):
            n = self.createAnd(n1, n2)
        elif(v1 == "*"):
            n = self.createCline(n1)
        elif(v1 == "+"):
            n = self.createPlus(n1)

        return n

    def createNode(self, v):
        init = self.newNode()
        empty = self.newNode()
        value = self.newNode()
        end = self.newNode()
        init.addEdge(empty, V_EMPTY)
        empty.addEdge(value, v)
        value.addEdge(end, V_EMPTY)
        init.last = end
        return init

    def createCline(self, n1):
        n1.last.addEdge(n1, V_EMPTY)
        n1.addEdge(n1.last, V_EMPTY)
        return n1

    def createPlus(self, n1):
        n1.last.addEdge(n1, V_EMPTY)
        return n1


    def createAnd(self, n1, n2):
        n1.last.addEdge(n2, V_EMPTY)
        n1.last = n2.last
        return n1


    def createOr(self, n1, n2):
        init = self.newNode()
        end = self.newNode()
        init.addEdge(n1,V_EMPTY)
        init.addEdge(n2,V_EMPTY)
        n1.last.addEdge(end,V_EMPTY)
        n2.last.addEdge(end,V_EMPTY)
        init.last = end
        return init


    def newNode(self, name = False):
        if(not name):
            global STATE
            STATE += 1
            name = 'Q' + str(STATE)
        n = MyNode(name)
        self.nodes.append(n)
        return n

    def print(self):
        print("\nInitial state: " + str(self.init.value))
        ends = ''
        if isinstance(self.ends,list):
            for e in self.ends:
                ends += e.value + " "
        else:
            ends = self.ends.value
        print("Final state: " + str(ends) + "\n")
        for n in self.nodes:
            for e in n.edges:
                print(str(n.value) + " => " +
                      str(e.value) + " -> " + str(e.to.value))
        print("\n")

    def plot(self):
        g = nx.MultiDiGraph()
        edge_labels = dict()
        color_map = []

        for n in self.nodes:
            if(n.init):
                color_map.append('y')
            elif(n.end):
                color_map.append('m')
            else:
                color_map.append('c')
            g.add_node(n.value)

        for n in self.nodes:
            for e in n.edges:
                g.add_edge(n.value, e.to.value)
                edge_labels[(n.value, e.to.value)] = e.value

        pos = nx.shell_layout(g)
        nx.draw(g, pos, with_labels=True, arrows=True, arrowsize=7, splines='curved',
                node_color=color_map, node_size=400, font_size=10)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
        blue = mpatches.Patch(color='y', label='Initial State')
        red = mpatches.Patch(color='m', label='Final State')
        plt.legend(handles=[blue, red])
        plt.show()


    #BUSCA EM PROFUNDIDADE
    def dfs(self, node, search = False, closure = []):
        if not isinstance(closure, MyQueue):
            raise Exception("Closure must be a queue!")
        node.visited = True
        for e in node.edges:
            if(((search != False and e.value == search) or search == False) and not e.to.visited):
                closure.enqueue(e.to)
                self.dfs(e.to, search, closure)
        return closure


    #RESETA OS NÓS VISITADOS
    def clearVisited(self):
        for n in self.nodes:
            n.visited = False


    #CRIA O CLOSURE DO AUTOMATO
    def getClosure(self, init):
        self.clearVisited()
        closure = MyQueue()
        closure.enqueue(init)
        closure = self.dfs(init, V_EMPTY, closure)
        self.clearVisited()
        return closure

    #TRANSFORMA EM DFA
    def dfa_edge(self, new_automata, init = False, prev_graph = {}, prev_node = None):
        init = self.init if not init else init
        
        #CRIA O CLOSURE
        closure = self.getClosure(init).toList()

        #CRIA O NOVO NÓ
        node = new_automata.newNode(init.value)

        #GRAFO PARA NOVOS ESTADOS
        graph = {}

        #PARA CADA LETRA DO ALFABETO
        for x in self.alphabet:
            graph[x] = []
            #PARA CADA NÓ NO CLOSURE
            for n in closure:
                self.clearVisited()
                #BUSCA TODOS OS ESTADOS A PARTIR DO NÓ N CONSUMINDO A LETRA X
                temp = self.dfs(n, x, MyQueue())
                #SE EXISTEM ESTADO, ADICIONA NO GRAFO
                if(temp.size() > 0):
                    graph[x] += temp.toList()
                #SE UM NÓ DO CLOSURE É FINAL, ENTÃO O NOVO NÓ TMB SERÁ
                if(n.end):
                    node.end = True
                    new_automata.ends.append(n)
                
        #SE FOR O NÓ INICIAL DO AUTOMATO, ENTÃO O NOVO NÓ TMB SERÁ
        if(init == self.init):
            node.init = True
            new_automata.init = node

        #PARA CADA (ALFABETO CONSUMIDO -> ESTADOS ALCANÇADOS) NO GRAFO GERADO
        for k, states in graph.items():
            #PARA CADA ESTADO
            for v in states:
                #SE O ESTADO ALCANÇADO FOR O MESMO DE ORIGEM, CRIA UMA EDGE PARA ELE MESMO 
                #A EDGE É CRIADA NO ESTADO ANTERIOR, CASO EXISTA
                if(v == init):
                    prev_node = prev_node if prev_node else node
                    node.addEdge(prev_node, k)
                #SE O ESTADO NÃO CONSOME A LETRA DO ALFABETO OU A MESMA NAO FOI CONSUMIDA NO ESTADO ANTERIOR
                elif(k not in prev_graph.keys() or v not in prev_graph[k]):
                    #VERIFICA SE O ESTADO JÁ NÃO ESTÁ NO NOVO AUTOMATO
                    jump = False
                    for x in new_automata.nodes:
                        if(x.value == v.value):
                            node.addEdge(x, k)
                            jump = True
                            break
                    if(jump):
                        continue
                    #REPETE O PROCEDIMENTO PARA O PROXIMO ESTADO
                    to = self.dfa_edge(new_automata, v, graph, node)
                    #SE EXISTEM SAIDAS DO PRÓXIMO ESTADO OU É UM ESTADO FINAL, ADICIONA UMA ARESTA PARA ELE
                    if(len(to.edges) > 0 or to.end):
                         node.addEdge(to, k)

        #RETORNA O NÓ
        return node
        

    def dfa(self):
        dfa = Automata()
        node = self.dfa_edge(dfa)
        node.init = True
        remove = []
        #REMOVE ESTADOS SEM SAÍDAS DO AUTOMATO
        for n in dfa.nodes:
            if(len(n.edges) == 0 and not n.end):
                remove.append(n)
        for n in remove:
            dfa.nodes.remove(n)
        #REMOVE FINAIS DUPLICADOS
        dfa.ends = list(set(dfa.ends))
        return dfa
