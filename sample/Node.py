from sample.CongruenceClosure import CongruenceClosure as cc
from sample import Main

class Node:

    id_value = 0

    def __init__(self, fn, args, ccpar):
        #increase the id
        self.id = self.get_new_id()
        #instance the attributes
        self.fn = fn
        self.args = args
        self.find = self.id
        self.ccpar = ccpar

    #getter & setter
    def get_id(self):
        return self.id

    def get_fn(self):
        return self.fn

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

    def __str__(self):
        return "id: {0}; \nfn: {1}; \nargs: {2}; \nccpar: {3}".format(self.id, self.fn, self.args, self.ccpar)

    #get unique id
    def get_new_id(self):
        type(self).id_value += 1
        return type(self).id_value

    #add the created node at the main list of nodes





