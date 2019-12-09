'''
input syle - theory of equality: f(a) = f(b), f(f(a)) = f(b), a != b, f(f(f(a))) != a
'''

def theory_of_equality_input_parser(text):
    #sanitize string
    text = text.strip()
    #split at the dot comma
    equations = text.split(';')
    sf = []
    for eq in equations:
        #aggiungo il termine alla lista di sottotermini:
        sf.append(eq)
        subs = rec_have_subterms(eq, [])
        sf.extend(subs)
    print(sf)


def rec_have_subterms(text, subs):
    #extract position of first (
    i = text.index('(')
    text = text[i+1:]
    subs.append(text)
    if '(' not in text:
        text.replace(')', ' ')
        return subs
    else:
        return rec_have_subterms(text, subs)


def main():
    theory_of_equality_input_parser("f(f(f(a)))")


if __name__ == "__main__":
    main()