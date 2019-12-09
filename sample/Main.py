from sample.Node import Node
from sample.CongruenceClosure import CongruenceClosure
import sample.InputParser as parser

def main():

    parser.theory_of_equality_input_parser("f(a) = f(b), f(f(a)) = f(b), a != b")

    cc = CongruenceClosure()
    n1 = Node("f", [2], [])
    n2 = Node("a", [], [1])
    cc.add_node(n1)

    cc.add_node(n2)

    cc.union(1, 2)
    print(cc)
    print('\n')
    print("hello")


if __name__ == "__main__":
    main()

