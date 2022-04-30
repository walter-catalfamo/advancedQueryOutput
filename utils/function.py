import pandas as pd
from fuzzywuzzy import fuzz


def f1(string, s1split):
    string = string.split("AND", 1)
    partial = []
    for substring in string:
        if "!=" in substring:
            substring = substring.split("!=", 1)[1]
            partial.append(fuzz.ratio(s1split, substring))
        else:
            partial.append(0)
    return max(partial)


def f2(string, s1split):
    string = string.split("AND", 1)
    partial = []
    for substring in string:
        partial.append(f3(substring, s1split))
    return max(partial)


def f3(substring, s1split):
    if "=" in substring:
        if "!=" not in substring and "<" not in substring:
            substring = substring.split("=", 1)[1]
            return fuzz.ratio(s1split, substring)
        else:
            return 0
    else:
        return 0


def calculation_and(first, second):
    tot = []
    if "!=" in first:
        s1split = first.split("!=", 1)[1]
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                res = []
                s_or = piece.split("OR", 1)
                for string in s_or:
                    if "AND" in string:
                        res.append(f1(string, s1split))
                    else:
                        if "!=" in string:
                            string = string.split("!=", 1)[1]
                            res.append(fuzz.ratio(s1split, string))
                        else:
                            res.append(0)
                tot.append(max(res))
            elif "AND" in piece:
                tot.append(f1(piece, s1split))
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
                    s_or = piece.split("OR", 1)
                    for string in s_or:
                        if "AND" in string:
                            res.append(f2(string, s1split))
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
                    tot.append(f2(piece, s1split))
                else:
                    tot.append(f3(piece, s1split))
            return max(tot)
        else:
            s1split = first.split("=", 1)[1]
            s1split = s1split.replace(" ", "")
            for piece in second:
                piece = piece.replace(")", "")
                if "OR" in piece:
                    res = []
                    s_or = piece.split("OR", 1)
                    for string in s_or:
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
                                    res.append(0)
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
                s_or = piece.split("OR", 1)
                for string in s_or:
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
        s1split = first.split("!=", 1)[1]
        s1attribute = first.split("!=", 1)[0]
        for piece in second:
            piece = piece.replace("(", "")
            piece = piece.replace(")", "")
            if "OR" in piece:
                s_or = piece.split("OR", 1)
                for string in s_or:
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
    elif "=" in first:
        if "<" not in first:
            s1split = first.split("=", 1)[1]
            s1attribute = first.split("=", 1)[0]
            for piece in second:
                piece = piece.replace("(", "")
                piece = piece.replace(")", "")
                if "OR" in piece:
                    s_or = piece.split("OR", 1)
                    for string in s_or:
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
                            increase_matrix(s1attribute, s2attribute, partial)
        else:
            s1split = first.split("=", 1)[1]
            s1split = s1split.replace(" ", "")
            s1attribute = first.split("<", 1)[0]
            for piece in second:
                piece = piece.replace("(", "")
                piece = piece.replace(")", "")
                if "OR" in piece:
                    s_or = piece.split("OR", 1)
                    for string in s_or:
                        if "AND" in string:
                            string = string.split("AND", 1)
                            for substring in string:
                                if "<" in substring:
                                    s2attribute = substring.split("<", 1)[0]
                                    substring = substring.split("=", 1)[1]
                                    substring = substring.replace(" ", "")
                                    if float(s1split) <= float(substring):
                                        partial = 100
                                    else:
                                        partial = 0  # da decidere
                                    increase_matrix(s1attribute, s2attribute, partial)
                                elif ">" in substring:
                                    s2attribute = substring.split(">", 1)[0]
                                    substring = substring.split(">", 1)[1]
                                    substring = substring.replace(" ", "")
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
                        if float(s1split) < float(string):
                            partial = 100
                        else:
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
    else:
        s1attribute = first.split(">", 1)[0]
        s1split = first.split(">", 1)[1]
        s1split = s1split.replace(" ", "")
        for piece in second:
            piece = piece.replace("(", "")
            piece = piece.replace(")", "")
            if "OR" in piece:

                s_or = piece.split("OR", 1)
                for string in s_or:
                    if "AND" in string:
                        string = string.split("AND", 1)
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
    matrix = pd.read_csv("data/matrix.csv")
    first = first.replace(" ", "")
    second = second.replace(" ", "")
    row = 0
    col = 0
    for i in range(len(matrix.columns)):
        if matrix.columns[i] == second:
            col = i
    for i in range(len(matrix.index)):
        r = matrix.index[i].replace(" ", "")
        if r == first:
            row = i
    matrix.loc[matrix.index[row], matrix.columns[col]] += 1 * (per / 100)
    matrix.to_csv("data/matrix.csv", index_label=False)
