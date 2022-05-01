from fuzzywuzzy import fuzz

from utils.matrix import increase_matrix


def f1a(substring, s1split):
    if "!=" in substring:
        substring = substring.split("!=", 1)[1]
        return fuzz.ratio(s1split, substring)
    else:
        return 0


def f1(string, s1split):
    string = string.split("AND", 1)
    partial = []
    for substring in string:
        partial.append(f1a(substring, s1split))
    return partial


def f2a(substring, s1split):
    if "=" in substring and "!=" not in substring and "<" not in substring:
        substring = substring.split("=", 1)[1]
        return fuzz.ratio(s1split, substring)
    else:
        return 0


def f2(string, s1split):
    string = string.split("AND", 1)
    partial = []
    for substring in string:
        partial.append(f2a(substring, s1split))
    return partial


def ff1a(substring, s1split, switch):
    if switch == 1:
        return f1a(substring, s1split)
    elif switch == 2:
        return f2a(substring, s1split)
    elif switch == 3:
        return f3(substring, s1split)


def ff1(string, s1split, switch):
    string = string.split("AND", 1)
    partial = []
    for substring in string:
        partial.append(ff1a(substring, s1split, switch))
    return partial


def f3a(string, s1split):
    if "<" in string:
        string = string.split("=", 1)[1]
        string = string.replace(" ", "")
        if float(s1split) < float(string):
            return 100
        else:
            return 0  # it was 100 before
    elif ">" in string:
        string = string.split(">", 1)[1]
        string = string.replace(" ", "")
        if float(s1split) < float(string):
            return 0
        else:
            return 100
    else:
        return 0


def f3(piece, s1split):
    res = []
    s_or = piece.split("OR", 1)
    for string in s_or:
        if "AND" in string:
            string = string.split("AND", 1)
            partial = []
            for substring in string:
                partial.append(f3a(substring, s1split))
            res.append(max(partial))
        else:
            res.append(f3a(string, s1split))
    return max(res)


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
                        res.append(max(f1(string, s1split)))
                    else:
                        res.append(f1a(string, s1split))
                tot.append(max(res))
            elif "AND" in piece:
                tot.append(max(f1(piece, s1split)))
            else:
                tot.append(f1a(piece, s1split))
    elif "=" in first and "<" not in first:
        s1split = first.split("=", 1)[1]
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                res = []
                s_or = piece.split("OR", 1)
                for string in s_or:
                    if "AND" in string:
                        res.append(max(f2(string, s1split)))
                    else:
                        res.append(f2a(string, s1split))
                tot.append(max(res))
            elif "AND" in piece:
                tot.append(max(f2(piece, s1split)))
            else:
                tot.append(f2a(piece, s1split))
    else:
        s1split = first.split(">", 1)[1]
        s1split = s1split.replace(" ", "")
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                tot.append(f3(piece, s1split))
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    partial.append(f3a(substring, s1split))
                tot.append(max(partial))
            else:
                tot.append(f3a(piece, s1split))
    return max(tot)


""""""""""""""""""


def f6(string, s1split, s1attribute, matrix):
    string = string.split("AND", 1)
    for substring in string:
        if "!=" in substring:
            s2attribute = substring.split(" !=", 1)[0]
            substring = substring.split("!=", 1)[1]
            partial = fuzz.ratio(s1split, substring)
            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def f7(string, s1split, s1attribute, matrix):
    string = string.split("AND", 1)
    for substring in string:
        matrix = f8(substring, s1split, s1attribute, matrix)
    return matrix


def f8(string, s1split, s1attribute, matrix):
    if "=" in string:
        if "!=" not in string and "<" not in string:
            s2attribute = string.split(" =", 1)[0]
            string = string.split("=", 1)[1]
            partial = fuzz.ratio(s1split, string)
            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def f14(string, s1split, s1attribute, s2attribute, matrix):
    string = string.replace(" ", "")
    if float(s1split) < float(string):
        partial = 100
    else:
        partial = 0
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def f9(substring, s1split, s1attribute, matrix):
    s2attribute = substring.split(">", 1)[0]
    substring = substring.split(">", 1)[1]
    matrix = f14(substring, s1split, s1attribute, s2attribute, matrix)
    return matrix


def f10(string, s1split, s1attribute, matrix):
    s2attribute = string.split("<", 1)[0]
    string = string.split("=", 1)[1]
    matrix = f14(string, s1split, s1attribute, s2attribute, matrix)
    return matrix


def f11(string, s1split, s1attribute, matrix):
    string = string.split("AND", 1)
    for substring in string:
        matrix = f12(substring, s1split, s1attribute, matrix)
    return matrix


def f12(string, s1split, s1attribute, matrix):
    if "<" in string:
        s2attribute = string.split(" <", 1)[0]
        string = string.split("=", 1)[1]
        string = string.replace(" ", "")
        if float(s1split) < float(string):
            partial = 100
        else:
            partial = 0
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    elif ">" in string:
        matrix = f13(string, s1split, s1attribute, matrix)
    return matrix


def f13(string, s1split, s1attribute, matrix):
    s2attribute = string.split(" >", 1)[0]
    string = string.split(">", 1)[1]
    string = string.replace(" ", "")
    if float(s1split) < float(string):
        partial = 100
    else:
        partial = 100
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute(first, second, matrix):
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
                        matrix = f6(string, s1split, s1attribute, matrix)
                    else:
                        if "!=" in string:
                            s2attribute = string.split(" !=", 1)[0]
                            string = string.split("!=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
            elif "AND" in piece:
                matrix = f6(piece, s1split, s1attribute, matrix)
            else:
                if "!=" in piece:
                    s2attribute = piece.split(" !=", 1)[0]
                    string = piece.split("!=", 1)[1]
                    partial = fuzz.ratio(s1split, string)
                    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
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
                            matrix = f7(string, s1split, s1attribute, matrix)
                        else:
                            matrix = f8(string, s1split, s1attribute, matrix)
                elif "AND" in piece:
                    matrix = f7(piece, s1split, s1attribute, matrix)
                else:
                    matrix = f8(piece, s1split, s1attribute, matrix)
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
                                    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                                elif ">" in substring:
                                    matrix = f9(substring, s1split, s1attribute, matrix)
                        else:
                            if "<" in string:
                                matrix = f10(string, s1split, s1attribute, matrix)
                            elif ">" in string:  # se nel target ho > invece di <=
                                s2attribute = string.split(">", 1)[0]
                                string = string.split(">", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    partial = 100
                                else:
                                    partial = 100
                                matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    for substring in string:
                        if "<" in substring:
                            matrix = f10(substring, s1split, s1attribute, matrix)
                        elif ">" in substring:
                            matrix = f9(substring, s1split, s1attribute, matrix)
                else:
                    if "<" in piece:
                        matrix = f10(piece, s1split, s1attribute, matrix)
                    elif ">" in piece:  # se nel target ho > invece di <=
                        s2attribute = piece.split(" >", 1)[0]
                        string = piece.split(">", 1)[1]
                        string = string.replace(" ", "")
                        if float(s1split) < float(string):
                            partial = 0  # in questo caso i due intervalli non hanno intersezioni
                        else:
                            partial = 100
                        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
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
                        matrix = f11(string, s1split, s1attribute, matrix)
                    else:
                        matrix = f12(string, s1split, s1attribute, matrix)
            elif "AND" in piece:
                matrix = f11(piece, s1split, s1attribute, matrix)
            else:
                if "<" in piece:
                    s2attribute = piece.split(" >", 1)[0]
                    string = piece.split("=", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        partial = 100
                    else:
                        partial = 0
                    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                elif ">" in piece:
                    matrix = f13(piece, s1split, s1attribute, matrix)
    return matrix
