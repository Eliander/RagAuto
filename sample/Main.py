from sample.Graph import Graph
import sample.InputParser as parser

formula = '!atom(w);i1 = j; i2 != i1; select(store(store(a, i1, v1), i2, v2), j) != select(a, j); select(a, j) = v1;'
#formula = "f(b) = b; f(f(b)) != car(cdr(cons(f(b), cons(b,d))));"
PRINTS = True
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
        li = line.split('#')
        print("{0}: {1}".format(count, li[0].strip()))
        terms, fn_to_index, new_formula = parser.extract_terms(li[0])
        count += 1

        graph = Graph(fn_to_index)
        graph.build_graph(terms)
        new_formula = new_formula.replace(' ', '')
        graph.congruence_closure(new_formula)
        print('Expected: {0}'.format(li[1]))


if __name__ == "__main__":
    if formula != '':
        main()
    else:
        read_inputs()

