from sample.Node import Node
from sample.CongruenceClosure import CongruenceClosure
import sample.InputParser as parser
import networkx as nx

def main():

    singletons = parser.extract_terms("f(a, b) = a; f(f(a, b), b) != a")

    nodes = []

    for sin in singletons.values():
        nodes.append(sin)
    cc = CongruenceClosure()
    for node in nodes:
        cc.add_node(node)

    cc.build_graph()

    print(cc)
    print('\n')
    print("hello")


if __name__ == "__main__":
    main()

