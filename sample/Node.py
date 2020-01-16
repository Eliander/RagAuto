from sample.Graph import Graph as cc
from sample import Main

class Node:

    id_value = 0

    def __init__(self, fn, id):
        self.id = id
        # instance the attributes
        self.fn = fn
        self.sym = fn[0]
        self.args = set()
        self.ccpar = set()
        self.find = self.id

    # getter & setter
    def get_id(self):
        return self.id

    def get_fn(self):
        return self.fn

    def get_sym(self):
        return self.sym

    def get_args(self):
        return self.args

    def get_find(self):
        return self.find

    def get_ccpar(self):
        return self.ccpar

    def set_find(self, new_find):
        self.find = new_find

    def set_ccpar(self, new_ccpar):
        self.ccpar = new_ccpar

    def set_args(self, new_args):
        self.args = new_args

    def __str__(self):
        return "id: {0}; \nfn: {1} ({2}); \nargs: {3}; \nccpar: {4}; \nfind: {5}\n\n".format(self.id, self.fn, self.sym, self.args, self.ccpar, self.find)

    #add the created node at the main list of nodes





