from sample.Graph import Graph
import sample.InputParser as parser

def main():

    '''
    f(a, b) = a; f(f(a, b), b) != a
    f(g(a)) = g(f(a)); f(g(f(b))) = a; f(b) = a; g(f(a)) != a
    f(f(f(a))) = f(f(a)); f(f(f(f(a)))) = a; f(a) != a
    f(x, y) = f(y, x); f(a, y) != f(y, a)
    f(g(x)) = g(f(x)); f(g(f(y))) = x; f(y) = x; g(f(x)) != x
    f(a, b) = a; f(f(a, b), b) != a
    f(f(f(a))) = f(a); f(f(a)) = a; f(a) != a
    f(x) = f(y); f(f(x)) = f(x); f(f(y)) != f(f(x))
    !atom(x); !atom(y); car(x) = car(y); cdr(x) = cdr(y); f(x) != f(y)
    f(b) = b; f(f(b)) != car(cons(f(b), d))
    '''

    #formula = "f(a, b) = a; f(f(a, b), b) != a"
    #formula = "f(g(a)) = g(f(a)); f(g(f(b))) = a; f(b) = a; g(f(a)) != a"
    formula = "f(f(f(a))) = f(f(a)); f(f(f(f(a)))) = a; f(a) != a"
    #formula = "f(x, y) = f(y, x); f(a, y) != f(y, a)" #errore -> soddisfacibile ma è insoddisfacibile

    #formula = "f(g(x)) = g(f(x)); f(g(f(y))) = x; f(y) = x; g(f(x)) != x"
    #formula = "f(a, b) = a; f(f(a, b), b) != a"
    #formula = "f(f(f(a))) = f(a); f(f(a)) = a; f(a) != a"
    #formula = "p(x); f(f(x)) = x; f(f(f(x))) = x; not[p(f(x))]" #error -> non gestito
    #formula = "f(x) = f(y); f(f(x)) = f(x); f(f(y)) != f(f(x))"

    #formula = "!atom(x); !atom(y); car(x) = car(y); cdr(x) = cdr(y); f(x) != f(y)"
    #formula = "f(b) = b; f(f(b)) != cons(f(b), d)" -> da sistemare estrazione termini
    terms, fn_to_index, new_formula = parser.extract_terms(formula)

    graph = Graph(fn_to_index)
    graph.build_graph(terms)
    new_formula = new_formula.replace(' ', '')
    graph.congruence_closure(new_formula)
    print('----------------------------------------------------')
    print(graph)
    print('----------------------------------------------------')


def readInputs():
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
    readInputs()

