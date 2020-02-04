from sample.Graph import Graph
import sample.InputParser as ccParser
import argparse
import time


def main(clauses, det, plt):
    terms, fn_to_index, new_formula = ccParser.extract_terms(clauses)
    launch_cc(terms, fn_to_index, new_formula, det, plt)


def read_inputs(det, plt):
    file = open('sample/inputs.txt', 'r')
    lines = file.readlines()

    count = 0
    for line in lines:
        li = line.split('#')
        print("{0}: {1}".format(count, li[0].strip()))
        start_time = time.time()
        terms, fn_to_index, new_formula = ccParser.extract_terms(li[0])
        count += 1
        launch_cc(terms, fn_to_index, new_formula, det, plt)
        print("--- %s seconds ---" % (time.time() - start_time))
        print('Expected: {0}'.format(li[1]))
        print('----------------------------------------------------')


def launch_cc(terms, fn_to_index, new_formula, det, plt):
    for idx in range(0, len(new_formula)):
        graph = Graph(fn_to_index[idx], det, plt)
        graph.build_graph(terms[idx])
        new_f = new_formula[idx].replace(' ', '')
        graph.congruence_closure(new_f)
        if graph.output == 'Soddisfacibile':
            break
    if len(new_formula) > 1:
        print('Risultato finale: {0}'.format(graph.output))
        print('----------------------------------------------------')


if __name__ == "__main__":
    parser= argparse.ArgumentParser(description='Congruence closure - Piacentini Elia - VR448249')

    parser.add_argument('--clauses', '-c', default='', help='set of clauses')
    parser.add_argument('--details', '-d', default=False, type=bool, help='shows detailed actions')
    parser.add_argument('--plot', '-p', default=False, type=bool, help='prints the plot if the set is satisfiable')
    args = parser.parse_args()

    # Load model
    clauses_set = args.clauses
    details = args.details
    plot = args.plot
    if clauses_set != '':
        main(clauses_set, details, plot)
    else:
        read_inputs(details, plot)