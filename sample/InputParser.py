# -*- coding: utf-8 -*-
"""InputParser.py

Questa classe viene utilizzata per parserizzare l'input estraendo i termini da analizzare
utilizzando l'algoritmo di chiusura di congruenza.

Attributi:
    index (int): variabile che permette di generare un identificativo univoco per ogni nodo
    terms_list [](String): lista di termini utilizzati nella teoria delle liste
    terms_array [](String): lista di termini utilizzati nella teoria degli array

Todo:
    * testare il tutto quando si inseriscono i termini formati da più caratteri.
    * aggiungere la chiusura di congruenza per gli array.
    * resettare l'indice una volta terminata una chiusura di congruenza
    * interfaccia grafica per inserimento della formula da testare e per la visualizzazione dell'output

"""
from sample.Node import Node

index = 0
terms_list = ['car', 'cdr', 'cons', 'atom', '!atom']
terms_array = ['store', 'select']


def save_subterm(open, close, text):
    """
        Funzione che estrae il successivo sottotermine

        Args:
            open: indici a cui si trova il carattere '(' nel testo in analisi.
            close: indici a cui si trova il carattere ')' nel testo in analisi.
            text: testo in analisi.

        Returns:
            Una stringa contenente il sottotermine

    """
    if len(open) > 1:
        # se non è più lunga di 1 significa che devo prendere tutto il termine
        text_in_par = text[open[-1]: close[-1]+1]
        index = open[-1] -1
        while text[index] != ',' and text[index] != '(':
            index -= 1
        return text[index + 1: close[-1]+1]
    else:
        return text[:close[-1]+1]


def have_subterms(text, sf):
    """
        Funzione che controlla se il termine dei sottotermini.

        Args:
            text: termine da cui estrarre i sottotermini (se esistono).
            sf: partizione contenente le classi singoletto.

        Returns:
            Una mappa aggiornata delle classi singoletto

    """
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
            sub_term = save_subterm(open, close, text)
            is_present = False
            for j in sf.values():
                if j.get_fn() == sub_term:
                    is_present = True
            if not is_present:
                index = get_index()
                map[index] = Node(sub_term, index)
            # cancello le parentesi che ho salvato dalle liste
            if len(open) > 0:
                open.remove(open[-1])
            if len(close) > 0:
                close.remove(close[-1])
    return map


def extract_terms(text):
    """
        Funzione che etrae i termini dall'equazione.

        Example:
            car(x) = car(y); cdr(x) = cdr(y); f(x) = f(y); !atom(x); !atom(y)
                car(x), car(y), cdr(x), cdr(y), f(x), f(y), cons(u1, v1), cons(u2, v2), x, y

        Args:
            text: equazione da cui estrarre i termini.

        Returns:
            Una mappa aggiornata delle classi singoletto
            Una mappa id -> simbolo del nodo
            Una stringa col testo in input a cui sono state applicate le trasformazioni necessarie
    """
    # sanitize string
    text = text.strip()
    text = text.replace(' ', '')
    # copia della stringa da ritornare: avra' i termini !atom cambiati
    result = set()
    copy = text
    # replace di != e = con ;
    text = text.replace('!=', ';')
    text = text.replace('=', ';')
    # split al ;
    equations = text.split(';')
    sf = {}
    # conto gli elementi per ciclare
    length = len(equations)
    '''
    Per ogni equazione devo verificare se ho bisogno di applicare le trasformazioni. Mentre !atom e car/cdr mantengono
    una sola formula, con store e select posso averne più di una. Sposto quindi store-select fuori
    '''
    for i in range(0, length):
        copy_of_text = copy
        # se è un !atom devo aggiungere i relativi car e cdr
        if "!atom" in equations[i]:
            # estraggo la variabile
            var = equations[i][equations[i].index('(')+1:equations[i].index(')')]
            new_eq = '{0} = cons({1}, {2})'.format(var, var+'u', var+'v')
            new_car = '{0} = car(cons({1}, {2}));'.format(var+'u', var+'u', var+'v')
            new_cdr = '{0} = car(cons({1}, {2}));'.format(var + 'v', var + 'u', var + 'v')
            # rimuovo il vecchio elemento e aggiungo i due nuovi
            equations[i] = 'cons({0}, {1})'.format(var+'u', var+'v')
            equations.append(var)
            equations[i] = equations[i].replace('!atom({0})'.format(var), new_eq)
            equations.append('car(cons({1}, {2}))'.format(var+'u', var+'u', var+'v'))
            equations.append('car(cons({1}, {2}))'.format(var + 'v', var + 'u', var + 'v'))
            # sostituisco anche nella string di ritorno con la formula completa
            copy_of_text = copy_of_text.replace('!atom({0})'.format(var), new_eq)
            copy_of_text = copy_of_text + new_car + new_cdr
        # se ci sono dei cons li sostituisco con le necessarie equazioni
        if "cons" in equations[i]:
            # estraggo i cons
            conses = []
            for j in range(0, len(equations[i])):
                if equations[i][j:j+4] == 'cons':
                    var = ''
                    var = variable_of_term(equations[i], j, len('cons'))
                    conses.append(var)
            # per ogni cons faccio i relativi car e cdr
            for cons in conses:
                parenthesis = 0
                idx_var = 4
                # devo cercare la virgola dove splittare
                while parenthesis != 1 or equations[i][idx_var] != ')':
                    if cons[idx_var] == '(':
                        parenthesis += 1
                    elif cons[idx_var] == ')':
                        parenthesis -= 1
                    elif cons[idx_var] == ',' and parenthesis == 1:
                        break
                    idx_var += 1
                car = cons[5:idx_var]
                cdr = cons[idx_var+1:]
                # elimino le parentesi in eccesso nel cdr
                parenthesis = 0
                for j in range(0, len(cdr)):
                    if cdr[j] == '(':
                        parenthesis += 1
                    elif cdr[j] == ')':
                        parenthesis -= 1
                    if parenthesis == 0 and cdr[j] == ')':
                        j +=1
                        break
                cdr = cdr[:j]
                # aggiungo car e cdr al testo
                copy_of_text += car + '=' + 'car(' + cons + ');'
                copy_of_text += cdr + '=' + 'cdr(' + cons + ');'
        # se è una store con una select applico r-o-w-1 e r-o-w-2, se è una select la sostituisco con un nuovo termine
        if "select" in equations[i]:
            # estraggo i read-over-write
            stores = []

            # quando splitto ottengo sempre #store + 1 elementi nell'array
            for j in range(0, len(equations[i])):
                if equations[i][j:j + len('store')] == 'store':
                    var = variable_of_term(equations[i], j, len('store'))
                    stores.append(var)
            # per ogni r-o-w valuto i casi = e !=
            for row in stores:
                copy_of_text = copy
                parenthesis = -1
                # partendo dal fondo, prendo il valore da inserire : funziona anche se ho una select
                idx_var = len(row) - 2
                # devo cercare la virgola dove splittare per recuperare l'index store
                # to do: devo cercare su equazione non su row
                while parenthesis != 0 and row[idx_var] != ',':
                    if row[idx_var] == '(':
                        parenthesis += 1
                    elif row[idx_var] == ')':
                        parenthesis -= 1
                    idx_var -= 1
                # elimino la virgola e la parentesi finale
                value_store = row[idx_var+1:-1]
                # estraggo l'indice
                pieces = row[:idx_var].split(',')
                index_store = pieces[-1].replace(')', '')
                # estraggo lo store name
                store_name = get_store_name(row)
                # ora prendo l'indice della select
                parenthesis = 0
                # devo cercare la virgola dove splittare per recuperare l'index select
                for j in range(len(equations[i]) - 1, 0, -1):
                    if equations[i][j] == ',':
                        # salvo l'indice della select eliminando virgola e parentesi
                        index_select = equations[i][j + 1: -1]
                        break
                # le due nuove equazioni sono:
                    # select(.. , i) = .... ; i = j
                    # select(.. , i) = .... ; i != j
                new_r_o_w = '{0}'.format(value_store)
                indexes = '{0} = {1};'.format(index_select, index_store)
                # to do: manca la versione !=
                copy_of_text += indexes
                copy_of_text = copy_of_text.replace(equations[i], new_r_o_w)
                result.add(copy_of_text)
        result.add(copy_of_text)
    # risplitto le equazioni per portarmi dietro il preprocessing
    text = copy_of_text
    text = text.replace('!=', ';')
    text = text.replace('=', ';')
    equations = text.split(';')
    for eq in equations:
        # sostituisco !atom
        map = have_subterms(eq, sf)
        sf = merge_dict(sf, map)
    tmp = {}
    tmp.update(sf)
    to_add = set()
    for term in tmp.values():
        get_single_terms(term.get_fn(), to_add)
    to_add = list(to_add)
    to_add.sort()
    for el in to_add:
        idx = get_index()
        sf[idx] = Node(el, idx)
    fn_to_index = populate_ccpar(sf)
    return sf, fn_to_index, list(result)


def get_store_name(text):
    parenthesis = 0
    store_name = ''
    text = text.replace('store(', '#', 1)
    if 'store(' in text:
        store_name = get_store_name(text)
    else:
        splitted = text.split('#')
        for splitt in splitted:
            if splitt != '':
                store_name = splitt.split(',')[0]
    return store_name


def variable_of_term(equation, j, length):
    parenthesis = -1
    idx_var = j + length
    while parenthesis != 0:
        if equation[idx_var] == '(':
            if parenthesis == -1:
                parenthesis = 0
            parenthesis += 1
        elif equation[idx_var] == ')':
            if parenthesis == -1:
                parenthesis = 0
            parenthesis -= 1
        idx_var += 1
    return equation[j:idx_var]


def get_single_terms(term, arr):
    if '(' in term:
        if ')' in term:
            end = term.index(')', -1)+1
        else:
            end = len(term)
        term = term[term.index('(')+1:end]
        values = term.split(',')
        for v in values:
            get_single_terms(v, arr)
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
            left, right = copy[copy.index('(')+1:comma_index], copy[comma_index+1:copy.index(')', -1)]
            if left == subterm.get_fn() or right == subterm.get_fn():
                return True
    return False
