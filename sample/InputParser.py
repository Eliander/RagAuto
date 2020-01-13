'''
input syle - theory of equality: f(a) = f(b), f(f(a)) = f(b), a != b, f(f(f(a))) != a
'''

index = 1


def save_subterm(last_open, last_close, text):
    # estraggo il sottotermine
    return text[last_open - 1 : last_close]


def have_subterms(text):
    open = []
    close = []
    map = {}
    for i in range(0, len(text)):
        if text[i] == '(':
            # se e' una parentesi aperta mi salvo l'indice
            open.append(i)
        elif text[i] == ')':
            close.append(i)
            map[save_subterm(open[-1], close[-1]+1, text)] = get_index()
            # cancello le parentesi che ho salvato dalle liste
            open.remove(open[-1])
            close.remove(close[-1])
    return map


def theory_of_equality_input_parser(text):
    # sanitize string
    text = text.strip()
    # split at the dot comma
    equations = text.split(';')
    sf = {}
    for eq in equations:
        map = have_subterms(eq);
        sf = merge_dict(sf, map)
    tmp = {}
    tmp.update(sf)
    for term in tmp:
        sf = merge_dict(sf, rec_input_parser(term, sf));
    return sf


def get_index():
    global index
    index +=1
    return index -1


# se uso update cambia gli indici
def merge_dict(dict1, dict2):
    for key in dict2.keys():
        if key not in dict1.keys():
            dict1[key] = dict2[key]
    return dict1


def rec_input_parser(text, sf):
    # sanitize string
    text = text.strip()
    sub = rec_have_subterms(text, sf)
    for el in sub:
        if el not in sf.keys():
            sf[el] = get_index()
    return sf


def rec_have_subterms(text, subs):
    # extract position of first (
    i = text.index('(')
    text = text[i+1:]
    text = text.replace(' ', '')
    if '(' not in text:
        text = text.replace(')', '')
        # controllo se ha piuù termini
        l_text = text.split(',');
        return l_text
    else:
        return rec_have_subterms(text, subs)


def main():
    print(theory_of_equality_input_parser("f(g(h(a, w(b)),b)); g(f(a)); f(h(g(a, b), d), l(a, c))"))


if __name__ == "__main__":
    main()