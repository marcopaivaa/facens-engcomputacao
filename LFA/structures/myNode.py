from structures.myEdge import MyEdge


class MyNode:

    def __init__(self, value=None):
        self.value = value
        self.edges = []
        self.parent = None
        self.init = False
        self.end = False
        self.last = None
        self.visited = False

    def addEdge(self, to, value=None):
        for e in self.edges:
            if(e.to == to and e.value == value):
                return
        edge = MyEdge(to, value)        
        self.edges.append(edge)
