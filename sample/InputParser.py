'''
input style - theory of equality: f(a) = f(b), f(f(a)) = f(b), a != b, f(f(f(a))) != a
'''
from sample.CongruenceClosure import CongruenceClosure
from sample.Node import Node

index = 1


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


def extract_terms(text):
    # sanitize string
    text = text.strip()
    # replace != with ;
    text = text.replace('!=', ';')
    text = text.replace('=', ';')
    # split at the dot comma
    equations = text.split(';')
    sf = {}
    for eq in equations:
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
    populate_ccpar(sf)
    return sf


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
        if subterm.get_fn() != copy:
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
    cc = CongruenceClosure()
    for node in nodes:
        cc.add_node(node)
    print(cc)
    #print(extract_terms("f(a);f(f(a));f(a, b); f(f(a), w(b))"))


if __name__ == "__main__":
    main()