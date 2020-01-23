'''
input style - theory of equality: f(a) = f(b), f(f(a)) = f(b), a != b, f(f(f(a))) != a
'''
from sample.Graph import Graph
from sample.Node import Node

index = 0
term__array = ['car', 'cdr', 'cons', 'atom', '!atom']


def save_subterm(last_open, last_close, text):
    # estraggo il sottotermine
    return text[last_open - 1 : last_close]


def have_subterms(text, sf):
    open = []
    close = []
    map = {}
    text = text.replace(' ', '')
    for i in range(0, len(text)):
        if text[i] == '(':
            # se e' una parentesi aperta mi salvo l'indice
            open.append(i)
        elif text[i] == ')':
            close.append(i)
            subterm = ''
            for el in term__array:
                if el in text:
                    subterm = save_subterm(1, close[-1]+1, text)
                    break
            if subterm == '':
                subterm = save_subterm(open[-1], close[-1]+1, text)
            ispresent = False
            for j in sf.values():
                if j.get_fn() == subterm:
                    ispresent = True
            if not ispresent:
                index = get_index()
                map[index] = Node(subterm, index)
            # cancello le parentesi che ho salvato dalle liste
            open.remove(open[-1])
            close.remove(close[-1])
    return map

'''
Metodo che estrae i termini di una formula:
   - car(x) = car(y); cdr(x) = cdr(y); f(x) = f(y); !atom(x); !atom(y)
        car(x), car(y), cdr(x), cdr(y), f(x), f(y), cons(u1, v1), cons(u2, v2), x, y
'''
def extract_terms(text):
    # sanitize string
    text = text.strip()
    text = text.replace(' ', '')
    # copia della stringa da ritornare: avra' i termini !atom cambiati
    copy_of_text = text
    # replace di != e = con ;
    text = text.replace('!=', ';')
    text = text.replace('=', ';')
    # split al ;
    equations = text.split(';')
    sf = {}
    # conto gli elementi per ciclare
    length = len(equations)
    # sostituisco i !atom
    for i in range(0, length):
        if "!atom" in equations[i]:
            # estraggo la variabile
            var = equations[i][equations[i].index('(')+1:equations[i].index(')')]
            new_eq = '{0} = cons({1}, {2})'.format(var, var+'u', var+'v')
            # rimuovo il vecchio elemento e aggiungo i due nuovi
            equations[i] = 'cons({0}, {1})'.format(var+'u', var+'v')
            equations.append(var)
            equations[i] = equations[i].replace('!atom({0})'.format(var), new_eq)
            # sostituisco anche nella string di ritorno con la formula completa
            copy_of_text = copy_of_text.replace('!atom({0})'.format(var), new_eq)
    # splitto anche i cons
    for eq in equations:
        # sostituisco !atom
        map = have_subterms(eq, sf);
        sf = merge_dict(sf, map)
    tmp = {}
    tmp.update(sf)
    to_add = set()
    for term in tmp.values():
        get_subterms(term.get_fn(), to_add)
    for el in to_add:
        index = get_index()
        sf[index] = Node(el, index)
    fn_to_index = populate_ccpar(sf)
    # per ogni nodo cons, aggiungo un car ed un cdr e inserisco i relativi ccpar
    var = tmp.values()
    for term in var:
        if 'cons' in term.get_fn():
            car, cdr = build_car_cdr_for_cons(term);
            sf[car.id] = car;
            sf[cdr.id] = cdr;
            # metto nei ccpar di cons il car e il cdr appena creati
            sf[term.id].ccpar.add(car.id)
            sf[term.id].ccpar.add(cdr.id)
    return sf, fn_to_index, copy_of_text

def build_car_cdr_for_cons(term):
    nterm = term.fn[term.fn.index('(')+1: term.fn.index(')')]
    split = nterm.split(',')
    car = Node('car({0})'.format(split[0]), get_index())
    cdr = Node('cdr({0})'.format(split[1]), get_index())
    car.args.add(term.id)
    cdr.args.add(term.id)
    car.find = term.id
    cdr.find = term.id
    return car, cdr

def get_subterms(term, arr):
    if '(' in term:
        if ')' in term:
            end = term.index(')', -1)+1
        else:
            end = len(term)
        term = term[term.index('(')+1:end]
        values = term.split(',')
        for v in values:
            get_subterms(v, arr)
    else:
        arr.add(term.replace(')', ''))
        return arr


def get_index():
    global index
    index += 1
    return index - 1


# se uso update cambia gli indici
def merge_dict(dict1, dict2):
    for key in dict2.keys():
        if key not in dict1.keys():
            dict1[key] = dict2[key]
    return dict1


def populate_ccpar(sf):
    fn_to_index = {}
    for elem in sf.values():
        fn_to_index[elem.get_fn()] = elem.get_id()
    for el in fn_to_index.keys():
        for term in sf.values():
            if distance_one(sf.get(fn_to_index.get(el)), term.get_fn()):
                sf.get(fn_to_index.get(el)).ccpar.add(term.get_id())
                term.args.add(sf.get(fn_to_index.get(el)).get_id())
    return fn_to_index


def distance_one(subterm, term):
    copy = term
    comma_index = -1
    if subterm.get_fn() in copy:
        counter = 0
        if subterm.get_fn() != copy and \
                '(' in copy and ')' in copy: # funzione
            for j in range(0, len(copy)):
                if copy[j] == '(':
                    counter += 1
                elif copy[j] == ')':
                    counter -= 1
                if counter == 1 and copy[j] == ',':
                    comma_index = j
            l, r = copy[copy.index('(')+1:comma_index], copy[comma_index+1:copy.index(')', -1)]
            if l == subterm.get_fn() or r == subterm.get_fn():
                return True
    return False


def main():

    singletons = extract_terms("f(g(h(a, w(b)),b)); g(f(a)); g(f(a)); f(h(g(a, b), d), l(a, c))")
    nodes = []

    for sin in singletons.values():
        nodes.append(sin)
    cc = Graph()
    for node in nodes:
        cc.add_node(node)
    print(cc)
    # print(extract_terms("f(a);f(f(a));f(a, b); f(f(a), w(b))"))


if __name__ == "__main__":
    main()