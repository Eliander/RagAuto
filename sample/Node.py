from sample import Main


class Node:
    def __init__(self, fn, args, ccpar):
        self.id = self.getNewId()
        self.fn = fn
        self.args = args
        self.find = self.id
        self.ccpar = ccpar
        self.addThisNode()

    def __str__(self):
        return "id: {0}; \nfn: {1}; \nargs: {2}; \nccpar: {3}".format(self.id, self.fn, self.args, self.ccpar)

    #get unique id
    def getNewId(self):
        Main.id_value = Main.id_value + 1
        return Main.id_value

    #add the created node at the main list of nodes
    def addThisNode(self):
        Main.nodes[self.id] = self

    def node(id):
        return Main.nodes[id]

    def find(self, id):
        i = self.node(id)
        if self.find == i.id:
            return id
        else:
            self.Find(self.find)




