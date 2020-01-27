from sample.Graph import Graph
import sample.InputParser as parser

formula = "f(a, b) = a; f(f(a, b), b) != a;" # "i=j; i!=w; select(a, j) = v; select(store(store(a, i, v), w, z), j) != select(a, j);"

# formula = "!atom(x); !atom(y); car(x) = car(y); cdr(x) = cdr(y); f(x) != f(y);"


def main():
    terms, fn_to_index, new_formula = parser.extract_terms(formula)

    graph = Graph(fn_to_index)
    graph.build_graph(terms)
    new_formula = new_formula.replace(' ', '')
    graph.congruence_closure(new_formula)
    print('----------------------------------------------------')


def read_inputs():
    file = open('inputs.txt', 'r')
    lines = file.readlines()

    count = 0
    for line in lines:
        print("{0}: {1}".format(count, line.strip()))
        terms, fn_to_index, new_formula = parser.extract_terms(line)
        count += 1

        graph = Graph(fn_to_index)
        graph.build_graph(terms)
        new_formula = new_formula.replace(' ', '')
        graph.congruence_closure(new_formula)


if __name__ == "__main__":
    if formula != '':
        main()
    else:
        read_inputs()

