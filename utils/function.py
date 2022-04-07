from fuzzywuzzy import fuzz
import pandas as pd

"""questa funzione ritorna un valore che indica il rapporto di similarità di una stringa della sorgente
con le 3 stringhe del target"""


# in questa funzione a differenza dell'altra sto calcolando il risultato dell'and in un altro modo.
# se prima confrontavo la stringa della sorgente con entrambe le condizioni dell'and e ne facevo una media, adesso
# mi salvo solo il valore massimo perchè può essere che nella sorgente mi serva solo una condizione e quindi se nel
# target mi si verifica quella condizione da una parte dell'and devo tenerla buona così.

# rimuovo le parentesi dalle stringhe perchè potrebbero portare a risultati leggermente diversi durante il confronto.

# inoltre quando devo considerare il confronto tra interi rimuovo anche gli spazi nella stringa per poter ottenere una stringa
# con solo caratteri numerici e quindi avere un float.
def calculationAnd(first, second):
    tot = []
    if "!=" in first:
        # se ho != nella stringa della sorgente devo verificare che anche nel target abbia != se no non ha senso il confronto
        # e così per tutti gli altri casi, non posso confrontare stringhe che cercando condizioni diverse
        s1split = first.split("!=", 1)[1]
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                res = []
                sors = piece.split("OR", 1)
                for string in sors:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partial = []
                        for substring in string:
                            if "!=" in substring:
                                substring = substring.split("!=", 1)[1]
                                partial.append(fuzz.ratio(s1split, substring))
                            else:
                                partial.append(0)
                        res.append(max(partial))
                    else:
                        if "!=" in string:
                            string = string.split("!=", 1)[1]
                            res.append(fuzz.ratio(s1split, string))
                        else:
                            res.append(0)
                tot.append(max(res))
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    if "!=" in substring:
                        substring = substring.split("!=", 1)[1]
                        partial.append(fuzz.ratio(s1split, substring))
                    else:
                        partial.append(0)
                tot.append(max(partial))
            else:
                if "!=" in piece:
                    string = piece.split("!=", 1)[1]
                    tot.append(fuzz.ratio(s1split, string))
                else:
                    tot.append(0)
        return max(tot)
    # se nella sorgente ho "=" potrei esser nel caso di solo uguale o anche di minore uguale e quindi ho due casi da gestire
    elif "=" in first:
        # caso in cui ho solo "=" gestisco con il confrontro tra stringhe usando fuzz.ratio
        if "<" not in first:
            s1split = first.split("=", 1)[1]
            for piece in second:
                piece = piece.replace(")", "")
                if "OR" in piece:
                    res = []
                    sors = piece.split("OR", 1)
                    for string in sors:
                        if "AND" in string:
                            string = string.split("AND", 1)
                            partial = []
                            for substring in string:
                                if "=" in substring:
                                    if "!=" not in substring and "<" not in substring:
                                        substring = substring.split("=", 1)[1]
                                        partial.append(fuzz.ratio(s1split, substring))
                                    else:
                                        partial.append(0)
                                else:
                                    partial.append(0)
                            res.append(max(partial))
                        else:
                            if "=" in string:
                                if "!=" not in string and "<" not in string:
                                    string = string.split("=", 1)[1]
                                    res.append(fuzz.ratio(s1split, string))
                                else:
                                    res.append(0)
                            else:
                                res.append(0)
                    tot.append(max(res))
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    partial = []
                    for substring in string:
                        if "=" in substring:
                            if "!=" not in substring and "<" not in substring:
                                substring = substring.split("=", 1)[1]
                                partial.append(fuzz.ratio(s1split, substring))
                            else:
                                partial.append(0)
                        else:
                            partial.append(0)
                    tot.append(max(partial))
                else:
                    if "=" in piece:
                        if "!=" not in piece and "<" not in piece:
                            string = piece.split("=", 1)[1]
                            tot.append(fuzz.ratio(s1split, string))
                        else:
                            tot.append(0)
                    else:
                        tot.append(0)
            return max(tot)
        # se nella sorgente ho <= allora vado a controllare che anche nel target abbia <= o > e confronto gli intervalli
        # questo perchè una volta che ho verificato di avere <= o > vuol dire che sto trattando caratteri numerici
        else:
            s1split = first.split("=", 1)[1]
            s1split = s1split.replace(" ", "")
            for piece in second:
                piece = piece.replace(")", "")
                if "OR" in piece:
                    res = []
                    sors = piece.split("OR", 1)
                    for string in sors:
                        if "AND" in string:
                            string = string.split("AND", 1)
                            partial = []
                            for substring in string:
                                if "<" in substring:
                                    substring = substring.split("=", 1)[1]
                                    substring = substring.replace(" ", "")
                                    # in questo caso ho entrambi gli intervalli che devono essere minori di un valore quindi i due intervalli si intersecano
                                    # devo capire come valutare questa intersezione. Guardando il valore del target devo valutare il confrontro
                                    if float(s1split) <= float(substring):
                                        partial.append(100)
                                    else:
                                        partial.append(100)  # da decidere
                                elif ">" in substring:
                                    substring = substring.split(">", 1)[1]
                                    substring = substring.replace(" ", "")
                                    # in questo caso la sorgente è minore di un certo valore mentre il target è maggiore quindi posso avere che i due intervalli
                                    # non hanno intersezioni (quando il valore del target è maggiore) oppure che i due intervalli si intersichino
                                    if float(s1split) < float(substring):
                                        partial.append(0)  # niente intersezione
                                    else:
                                        partial.append(100)  # intersezione
                                else:
                                    partial.append(0)  # nel target non ho un valore numerico
                            res.append(max(partial))
                        else:
                            if "<" in string:
                                string = string.split("=", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    res.append(100)
                                else:
                                    res.append(100)
                            elif ">" in string:  # se nel target ho > invece di <=
                                string = string.split(">", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    res.append(0)
                                else:
                                    res.append(100)
                            else:
                                res.append(0)
                    tot.append(max(res))
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    partial = []
                    for substring in string:
                        if "<" in substring:
                            substring = substring.split("=", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial.append(100)
                            else:
                                partial.append(100)
                        elif ">" in substring:
                            substring = substring.split(">", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial.append(0)  # in questo caso i due intervalli non hanno intersezioni
                            else:
                                partial.append(100)
                        else:
                            partial.append(0)
                        tot.append(max(partial))
                else:
                    if "<" in piece:
                        string = piece.split("=", 1)[1]
                        string = string.replace(" ", "")
                        # devo controllare che gli intervalli siano simili, considero che se il numero del
                        # target è minore allora la somiglianza è 100?
                        if float(s1split) < float(string):
                            # i due intervalli hanno un intersezione con valore della sorgente minore
                            tot.append(100)
                        else:
                            # i due intervalli hanno un intersezione con valore del target minore
                            tot.append(100)
                    elif ">" in piece:  # se nel target ho > invece di <=
                        string = piece.split(">", 1)[1]
                        string = string.replace(" ", "")
                        if float(s1split) < float(string):
                            tot.append(0)  # in questo caso i due intervalli non hanno intersezioni
                        else:
                            tot.append(100)
                            # in questo caso gli intervali hanno un intersezione, come valuto?
                    else:
                        tot.append(0)
            return max(tot)
    # se nella stringa della sorgente ho ">" devo fare glis stessi ragionamenti che ho fatto con <= ma avrò condizioni
    # diverse a seconda di cosa mi si presenti nel target
    else:
        s1split = first.split(">", 1)[1]
        s1split = s1split.replace(" ", "")
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                res = []
                sors = piece.split("OR", 1)
                for string in sors:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partial = []
                        for substring in string:
                            if "<" in substring:
                                substring = substring.split("=", 1)[1]
                                substring = substring.replace(" ", "")
                                if float(s1split) < float(substring):
                                    # i due intervalli hanno un'intersezione
                                    partial.append(100)
                                else:
                                    # i due intervalli non hanno intersezione
                                    partial.append(0)
                            elif ">" in substring:
                                substring = substring.split(">", 1)[1]
                                substring = substring.replace(" ", "")
                                if float(s1split) < float(substring):
                                    # i due intervalli hanno un intersezione
                                    partial.append(100)
                                else:
                                    # i due intervalli hanno un intersezione
                                    partial.append(100)
                            else:
                                partial.append(0)
                        res.append(max(partial))
                    else:
                        if "<" in string:
                            string = string.split("=", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                res.append(100)
                            else:
                                res.append(0)
                        elif ">" in string:  # se nel target ho > invece di <=
                            string = string.split(">", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                res.append(100)
                            else:
                                res.append(100)
                        else:
                            res.append(0)
                tot.append(max(res))
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    if "<" in substring:
                        substring = substring.split("=", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial.append(100)
                        else:
                            partial.append(0)
                    elif ">" in substring:
                        substring = substring.split(">", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial.append(100)
                        else:
                            partial.append(100)
                    else:
                        partial.append(0)
                    tot.append(max(partial))
            else:
                if "<" in piece:
                    string = piece.split("=", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        tot.append(100)
                    else:
                        tot.append(0)
                elif ">" in piece:
                    string = piece.split(">", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        tot.append(100)
                    else:
                        tot.append(100)
                else:
                    tot.append(0)
        return max(tot)

    # con questa funzione andrò ad ottenere gli attributi che combaciano tra primo e secondo


def findAttribute(first, second):
    first = first.replace("(", "")
    if "!=" in first:
        # se ho != nella stringa della sorgente devo verificare che anche nel target abbia != se no non ha senso il confronto
        # e così per tutti gli altri casi, non posso confrontare stringhe che cercando condizioni diverse
        s1split = first.split("!=", 1)[1]
        s1attribute = first.split("!=", 1)[0]
        for piece in second:
            piece = piece.replace("(", "")
            piece = piece.replace(")", "")
            if "OR" in piece:
                sors = piece.split("OR", 1)
                for string in sors:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        for substring in string:
                            if "!=" in substring:
                                s2attribute = substring.split(" !=", 1)[0]
                                substring = substring.split("!=", 1)[1]
                                partial = fuzz.ratio(s1split, substring)
                                increase_matrix(s1attribute, s2attribute, partial)
                    else:
                        if "!=" in string:
                            s2attribute = string.split(" !=", 1)[0]
                            string = string.split("!=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            increase_matrix(s1attribute, s2attribute, partial)
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    if "!=" in substring:
                        s2attribute = substring.split(" !=", 1)[0]
                        substring = substring.split("!=", 1)[1]
                        partial = fuzz.ratio(s1split, substring)
                        increase_matrix(s1attribute, s2attribute, partial)
            else:
                if "!=" in piece:
                    s2attribute = string.split(" !=", 1)[0]
                    string = piece.split("!=", 1)[1]
                    partial = fuzz.ratio(s1split, string)
                    increase_matrix(s1attribute, s2attribute, partial)
                    # se nella sorgente ho "=" potrei esser nel caso di solo uguale o anche di minore uguale e quindi ho due casi da gestire
    elif "=" in first:
        # caso in cui ho solo "=" gestisco con il confrontro tra stringhe usando fuzz.ratio
        if "<" not in first:
            s1split = first.split("=", 1)[1]
            s1attribute = first.split("=", 1)[0]
            for piece in second:
                piece = piece.replace("(", "")
                piece = piece.replace(")", "")
                if "OR" in piece:
                    sors = piece.split("OR", 1)
                    for string in sors:
                        if "AND" in string:
                            string = string.split("AND", 1)
                            for substring in string:
                                if "=" in substring:
                                    if "!=" not in substring and "<" not in substring:
                                        s2attribute = substring.split(" =", 1)[0]
                                        substring = substring.split("=", 1)[1]
                                        partial = fuzz.ratio(s1split, substring)
                                        increase_matrix(s1attribute, s2attribute, partial)
                        else:
                            if "=" in string:
                                if "!=" not in string and "<" not in string:
                                    s2attribute = string.split(" =", 1)[0]
                                    string = string.split("=", 1)[1]
                                    partial = fuzz.ratio(s1split, string)
                                    increase_matrix(s1attribute, s2attribute, partial)
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    partial = []
                    for substring in string:
                        if "=" in substring:
                            if "!=" not in substring and "<" not in substring:
                                s2attribute = substring.split(" =", 1)[0]
                                substring = substring.split("=", 1)[1]
                                partial = fuzz.ratio(s1split, substring)
                                increase_matrix(s1attribute, s2attribute, partial)
                else:
                    if "=" in piece:
                        if "!=" not in piece and "<" not in piece:
                            s2attribute = piece.split(" =", 1)[0]
                            string = piece.split("=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            increase_matrix(s1attribute, s2attribute, partial, "data\matrix.csv")
                            # se nella sorgente ho <= allora vado a controllare che anche nel target abbia <= o > e confronto gli intervalli
        # questo perchè una volta che ho verificato di avere <= o > vuol dire che sto trattando caratteri numerici
        else:
            s1split = first.split("=", 1)[1]
            s1split = s1split.replace(" ", "")
            s1attribute = first.split("<", 1)[0]
            for piece in second:
                piece = piece.replace("(", "")
                piece = piece.replace(")", "")
                if "OR" in piece:
                    sors = piece.split("OR", 1)
                    for string in sors:
                        if "AND" in string:
                            string = string.split("AND", 1)
                            for substring in string:
                                if "<" in substring:
                                    s2attribute = substring.split("<", 1)[0]
                                    substring = substring.split("=", 1)[1]
                                    substring = substring.replace(" ", "")
                                    # in questo caso ho entrambi gli intervalli che devono essere minori di un valore quindi i due intervalli si intersecano
                                    # devo capire come valutare questa intersezione. Guardando il valore del target devo valutare il confrontro
                                    if float(s1split) <= float(substring):
                                        partial = 100
                                    else:
                                        partial = 0  # da decidere
                                    increase_matrix(s1attribute, s2attribute, partial)
                                elif ">" in substring:
                                    s2attribute = substring.split(">", 1)[0]
                                    substring = substring.split(">", 1)[1]
                                    substring = substring.replace(" ", "")
                                    # in questo caso la sorgente è minore di un certo valore mentre il target è maggiore quindi posso avere che i due intervalli
                                    # non hanno intersezioni (quando il valore del target è maggiore) oppure che i due intervalli si intersichino
                                    if float(s1split) < float(substring):
                                        partial = 0  # niente intersezione
                                    else:
                                        partial = 100  # intersezione
                                    increase_matrix(s1attribute, s2attribute, partial)
                        else:
                            if "<" in string:
                                s2attribute = string.split("<", 1)[0]
                                string = string.split("=", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    partial = 100
                                else:
                                    partial = 0
                                increase_matrix(s1attribute, s2attribute, partial)
                            elif ">" in string:  # se nel target ho > invece di <=
                                s2attribute = string.split(">", 1)[0]
                                string = string.split(">", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    partial = 100
                                else:
                                    partial = 100
                                increase_matrix(s1attribute, s2attribute, partial)
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    for substring in string:
                        if "<" in substring:
                            s2attribute = substring.split("<", 1)[0]
                            substring = substring.split("=", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial = 100
                            else:
                                partial = 0
                            increase_matrix(s1attribute, s2attribute, partial)
                        elif ">" in substring:
                            s2attribute = substring.split(">", 1)[0]
                            substring = substring.split(">", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial = 0  # in questo caso i due intervalli non hanno intersezioni
                            else:
                                partial = 100
                            increase_matrix(s1attribute, s2attribute, partial)
                else:
                    if "<" in piece:
                        s2attribute = piece.split("<", 1)[0]
                        string = piece.split("=", 1)[1]
                        string = string.replace(" ", "")
                        # devo controllare che gli intervalli siano simili, considero che se il numero del
                        # target è minore allora la somiglianza è 100?
                        if float(s1split) < float(string):
                            # i due intervalli hanno un intersezione con valore della sorgente minore
                            partial = 100
                        else:
                            # i due intervalli hanno un intersezione con valore del target minore
                            partial = 0
                        increase_matrix(s1attribute, s2attribute, partial)
                    elif ">" in piece:  # se nel target ho > invece di <=
                        s2attribute = piece.split(" >", 1)[0]
                        string = piece.split(">", 1)[1]
                        string = string.replace(" ", "")
                        if float(s1split) < float(string):
                            partial = 0  # in questo caso i due intervalli non hanno intersezioni
                        else:
                            partial = 100
                        increase_matrix(s1attribute, s2attribute, partial)
                        # in questo caso gli intervali hanno un intersezione, come valuto?
    # se nella stringa della sorgente ho ">" devo fare glis stessi ragionamenti che ho fatto con <= ma avrò condizioni
    # diverse a seconda di cosa mi si presenti nel target
    else:
        s1attribute = first.split(">", 1)[0]
        s1split = first.split(">", 1)[1]
        s1split = s1split.replace(" ", "")
        for piece in second:
            piece = piece.replace("(", "")
            piece = piece.replace(")", "")
            if "OR" in piece:

                sors = piece.split("OR", 1)
                for string in sors:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partial = []
                        for substring in string:
                            if "<" in substring:
                                s2attribute = substring.split(" <", 1)[0]
                                substring = substring.split("=", 1)[1]
                                substring = substring.replace(" ", "")
                                if float(s1split) < float(substring):
                                    # i due intervalli hanno un'intersezione
                                    partial = 100
                                else:
                                    # i due intervalli non hanno intersezione
                                    partial = 0
                                increase_matrix(s1attribute, s2attribute, partial)
                            elif ">" in substring:
                                s2attribute = substring.split(" >", 1)[0]
                                substring = substring.split(">", 1)[1]
                                substring = substring.replace(" ", "")
                                if float(s1split) < float(substring):
                                    # i due intervalli hanno un intersezione
                                    partial = 100
                                else:
                                    # i due intervalli hanno un intersezione
                                    partial = 100
                                increase_matrix(s1attribute, s2attribute, partial)
                    else:
                        if "<" in string:
                            s2attribute = string.split(" <", 1)[0]
                            string = string.split("=", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                partial = 100
                            else:
                                partial = 0
                            increase_matrix(s1attribute, s2attribute, partial)
                        elif ">" in string:  # se nel target ho > invece di <=
                            s2attribute = string.split(" >", 1)[0]
                            string = string.split(">", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                partial = 100
                            else:
                                partial = 100
                            increase_matrix(s1attribute, s2attribute, partial)
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    if "<" in substring:
                        s2attribute = substring.split(" <", 1)[0]
                        substring = substring.split("=", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial = 100
                        else:
                            partial = 0
                        increase_matrix(s1attribute, s2attribute, partial)
                    elif ">" in substring:
                        s2attribute = substring.split(" >", 1)[0]
                        substring = substring.split(">", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial = 100
                        else:
                            partial = 100
                        increase_matrix(s1attribute, s2attribute, partial)
            else:
                if "<" in piece:
                    s2attribute = piece.split(" >", 1)[0]
                    string = piece.split("=", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        partial = 100
                    else:
                        partial = 0
                    increase_matrix(s1attribute, s2attribute, partial)
                elif ">" in piece:
                    s2attribute = piece.split(" >", 1)[0]
                    string = piece.split(">", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        partial = 100
                    else:
                        partial = 100
                    increase_matrix(s1attribute, s2attribute, partial)


def increase_matrix(first, second, per):
    evaluate_new_matrix(first, second, pd.read_csv("data/matrix.csv"), per)


def increase_matrix(first, second, per, filename):
    evaluate_new_matrix(first, second, pd.read_csv(filename), per)


def evaluate_new_matrix(first, second, matrix, per):
    first = first.replace(" ", "")
    second = second.replace(" ", "")
    i = 0
    for i in range(len(matrix.columns)):
        if matrix.columns[i] == second:
            col = i
    i = 0
    for i in range(len(matrix.index)):
        r = matrix.index[i].replace(" ", "")
        if r == first:
            row = i
    matrix.loc[matrix.index[row], matrix.columns[col]] += 1 * (per / 100)
    matrix.to_csv("data/matrix.csv", index_label=False)
