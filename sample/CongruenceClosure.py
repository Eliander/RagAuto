import networkx as nx



class CongruenceClosure:
    def __init__(self):
        self.DAG = nx.Graph()
        self.nodes = {}

    def __str__(self):
        for n in self.nodes.values():
            print(n)
        return ""

    def add_node(self, node):
        self.nodes[node.id]=node

    def node(self, id):
        return self.nodes[id]

    def find(self, id):
        node = self.node(id)
        if node.get_find() == node.get_id():
            return id
        else:
            self.find(id=node.get_find())

    def union(self, id_1, id_2):
        node_1 = self.node(self.find(id_1))
        node_2 = self.node(self.find(id_2))
        node_1.set_find(node_2.get_find())
        node_2.set_ccpar(node_2.get_ccpar() + node_1.get_ccpar())
        node_1.set_ccpar([])





