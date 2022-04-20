from fuzzywuzzy import fuzz
from utils import matrix


def calculation_and(first, second):
    tot = []
    if "!=" in first:
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
    elif "=" in first:
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
                                    if float(s1split) <= float(substring):
                                        partial.append(100)
                                    else:
                                        partial.append(100)  # da decidere
                                elif ">" in substring:
                                    substring = substring.split(">", 1)[1]
                                    substring = substring.replace(" ", "")
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
                        if float(s1split) < float(string):
                            tot.append(100)
                        else:
                            tot.append(100)
                    elif ">" in piece:  # se nel target ho > invece di <=
                        string = piece.split(">", 1)[1]
                        string = string.replace(" ", "")
                        if float(s1split) < float(string):
                            tot.append(0)  # in questo caso i due intervalli non hanno intersezioni
                        else:
                            tot.append(100)
                    else:
                        tot.append(0)
            return max(tot)
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


def find_attribute(first, second):
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
                                matrix.increase_matrix(s1attribute, s2attribute, partial)
                    else:
                        if "!=" in string:
                            s2attribute = string.split(" !=", 1)[0]
                            string = string.split("!=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            matrix.increase_matrix(s1attribute, s2attribute, partial)
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    if "!=" in substring:
                        s2attribute = substring.split(" !=", 1)[0]
                        substring = substring.split("!=", 1)[1]
                        partial = fuzz.ratio(s1split, substring)
                        matrix.increase_matrix(s1attribute, s2attribute, partial)
            else:
                if "!=" in piece:
                    s2attribute = string.split(" !=", 1)[0]
                    string = piece.split("!=", 1)[1]
                    partial = fuzz.ratio(s1split, string)
                    matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                                        matrix.increase_matrix(s1attribute, s2attribute, partial)
                        else:
                            if "=" in string:
                                if "!=" not in string and "<" not in string:
                                    s2attribute = string.split(" =", 1)[0]
                                    string = string.split("=", 1)[1]
                                    partial = fuzz.ratio(s1split, string)
                                    matrix.increase_matrix(s1attribute, s2attribute, partial)
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    partial = []
                    for substring in string:
                        if "=" in substring:
                            if "!=" not in substring and "<" not in substring:
                                s2attribute = substring.split(" =", 1)[0]
                                substring = substring.split("=", 1)[1]
                                partial = fuzz.ratio(s1split, substring)
                                matrix.increase_matrix(s1attribute, s2attribute, partial)
                else:
                    if "=" in piece:
                        if "!=" not in piece and "<" not in piece:
                            s2attribute = piece.split(" =", 1)[0]
                            string = piece.split("=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                                    matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                                    matrix.increase_matrix(s1attribute, s2attribute, partial)
                        else:
                            if "<" in string:
                                s2attribute = string.split("<", 1)[0]
                                string = string.split("=", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    partial = 100
                                else:
                                    partial = 0
                                matrix.increase_matrix(s1attribute, s2attribute, partial)
                            elif ">" in string:  # se nel target ho > invece di <=
                                s2attribute = string.split(">", 1)[0]
                                string = string.split(">", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    partial = 100
                                else:
                                    partial = 100
                                matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                            matrix.increase_matrix(s1attribute, s2attribute, partial)
                        elif ">" in substring:
                            s2attribute = substring.split(">", 1)[0]
                            substring = substring.split(">", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial = 0  # in questo caso i due intervalli non hanno intersezioni
                            else:
                                partial = 100
                            matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                        matrix.increase_matrix(s1attribute, s2attribute, partial)
                    elif ">" in piece:  # se nel target ho > invece di <=
                        s2attribute = piece.split(" >", 1)[0]
                        string = piece.split(">", 1)[1]
                        string = string.replace(" ", "")
                        if float(s1split) < float(string):
                            partial = 0  # in questo caso i due intervalli non hanno intersezioni
                        else:
                            partial = 100
                        matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                                matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                                matrix.increase_matrix(s1attribute, s2attribute, partial)
                    else:
                        if "<" in string:
                            s2attribute = string.split(" <", 1)[0]
                            string = string.split("=", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                partial = 100
                            else:
                                partial = 0
                            matrix.increase_matrix(s1attribute, s2attribute, partial)
                        elif ">" in string:  # se nel target ho > invece di <=
                            s2attribute = string.split(" >", 1)[0]
                            string = string.split(">", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                partial = 100
                            else:
                                partial = 100
                            matrix.increase_matrix(s1attribute, s2attribute, partial)
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
                        matrix.increase_matrix(s1attribute, s2attribute, partial)
                    elif ">" in substring:
                        s2attribute = substring.split(" >", 1)[0]
                        substring = substring.split(">", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial = 100
                        else:
                            partial = 100
                        matrix.increase_matrix(s1attribute, s2attribute, partial)
            else:
                if "<" in piece:
                    s2attribute = piece.split(" >", 1)[0]
                    string = piece.split("=", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        partial = 100
                    else:
                        partial = 0
                    matrix.increase_matrix(s1attribute, s2attribute, partial)
                elif ">" in piece:
                    s2attribute = piece.split(" >", 1)[0]
                    string = piece.split(">", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        partial = 100
                    else:
                        partial = 100
                    matrix.increase_matrix(s1attribute, s2attribute, partial)
