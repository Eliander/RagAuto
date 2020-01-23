import networkx as nx
import itertools

class Graph:
    def __init__(self, index_map):
        self.DAG = {}
        self.index_map = index_map
        self.not_in_same_set = []

    def add_node(self, node):
        self.DAG[node.id] = node

    def node(self, identificator):
        return self.DAG[identificator]

    def ccpar(self, identificator):
        id_find = self.find(identificator)
        return self.DAG[id_find].get_ccpar()

    def find(self, identificator):
        node = self.DAG[identificator]
        if node.get_find() == node.get_id():
            return identificator
        else:
            return self.find(node.get_find())

    def union(self, id_1, id_2):
        print('UNION({0}, {1}) \n'.format(id_1, id_2))
        node_1 = self.DAG[self.find(id_1)]
        node_2 = self.DAG[self.find(id_2)]
        node_1.set_find(node_2.get_find())
        node_2.set_ccpar(node_2.get_ccpar().union(node_1.get_ccpar()))
        node_1.set_ccpar(set())
        # controllo se violo qualche legame
        if self.check_constraints():
            raise Exception('Insoddisfacibile')

    def congruent(self, id_1, id_2):
        print('CONGRUENT({0}, {1})): '.format(id_1, id_2))
        node_1 = self.DAG[id_1]
        node_2 = self.DAG[id_2]
        if node_1.get_sym() == node_2.get_sym() and len(node_1.get_args()) == len(node_2.get_args()):
            list_args1 = list(node_1.get_args())
            list_args2 = list(node_2.get_args())
            for i in range(0, len(list_args1)):
                if self.find(list_args1[i]) != self.find(list_args2[i]):
                    print('F \n')
                    return False
                elif self.find(list_args1[i]) != self.find(list_args2[i]) and list_args1[i].get_sym == 'cons':
                    print('F by axiom !atom \n')
                    return False
            print('T \n')
            return True
        print('F \n')
        return False

    def merge(self, id_1, id_2):
        print('MERGE({0},{1}) \n'.format(id_1, id_2))
        if self.find(id_1) != self.find(id_2):
            p_i1 = self.ccpar(id_1)
            p_i2 = self.ccpar(id_2)
            print('Pi_1 = {0}'.format(p_i1))
            print('Pi_2 = {0}'.format(p_i2))
            self.union(id_1, id_2)
            tuples = []
            for i in p_i1:
                for j in p_i2:
                    tuples.append((i, j))
            for i in tuples:
                if self.find(i[0]) != self.find(i[1]) and self.congruent(i[0], i[1]):
                    self.merge(i[0], i[1])

    def check_constraints(self):
        for t in self.not_in_same_set:
            id_1 = self.DAG[t[0]].get_id()
            id_2 = self.DAG[t[1]].get_id()
            # fn_1 = self.DAG[id_1].get_fn()   ---  and fn_1 == 'cons'
            if self.find(id_1) == self.find(id_2):
                print('Violazione clausola: {0} != {1} '.format(self.DAG[id_1].get_fn(), self.DAG[id_2].get_fn()))
                return True
        return False

    def build_graph(self, nodes):
        # aggiungo tutti i nodi al grafo
        for element in nodes:
            self.DAG[element] = nodes.get(element)

    def congruence_closure(self, formula):
        # NB: ricordati che bisogna implementare la merge su f, car, cdr
        equals = []
        not_equals = []
        split = formula.split(';')

        for equation in split:
            if '!=' in equation:
                not_equals.append(equation)
            else:
                equals.append(equation)

        for not_congruent in not_equals:
            neq = not_congruent.split('!=')
            self.not_in_same_set.append((self.index_map[neq[0]], self.index_map[neq[1]]))

        for equation in equals:
            split_eq = equation.split('=')
            print('{0} = {1}'.format(split_eq[0], split_eq[1]))
            self.merge(self.index_map[split_eq[0]], self.index_map[split_eq[1]])

        print('Soddisfacibile')

    def __str__(self):
        for n in self.DAG:
            print(self.DAG[n])
        return ""

