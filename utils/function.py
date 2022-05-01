from fuzzywuzzy import fuzz

from utils.matrix import increase_matrix


def calculation_and_f1(substring, s1split):
    if "!=" in substring:
        substring = substring.split("!=", 1)[1]
        return fuzz.ratio(s1split, substring)
    else:
        return 0


def calculation_and_f2(substring, s1split):
    if "=" in substring:  # if "=" in substring and "!=" not in substring and "<" not in substring:
        substring = substring.split("=", 1)[1]
        return fuzz.ratio(s1split, substring)
    else:
        return 0


def calculation_and_f3(string, s1split):
    string = string.split(">", 1)[1]
    if float(s1split) < float(string):
        return 0
    else:
        return 100


def calculation_and_f4(string, s1split):
    string = string.split("<", 1)[1]
    if float(s1split) < float(string):
        return 100
    else:
        return 0


def calculation_and_lvl4(query_switch, string, s1split):
    if query_switch == 1:
        return calculation_and_f1(string, s1split)
    elif query_switch == 2:
        return calculation_and_f2(string, s1split)
    elif query_switch == 3:
        return calculation_and_f3(string, s1split)
    elif query_switch == 4:
        return calculation_and_f4(string, s1split)


def calculation_and_lvl3(loop_switch, query_switch, string, s1split):
    if loop_switch:
        string = string.split("AND", 1)
        res = []
        for substring in string:
            res.append(calculation_and_lvl4(query_switch, substring, s1split))
        return max(res)
    else:
        return calculation_and_lvl4(query_switch, string, s1split)


def calculation_and_lvl2(second, query_switch, s1split):
    tot = []
    for piece in second:
        piece = piece.replace(")", "")
        if "OR" in piece:
            res = []
            s_or = piece.split("OR", 1)
            for string in s_or:
                if "AND" in string:
                    res.append(calculation_and_lvl3(True, query_switch, string, s1split))
                else:
                    res.append(calculation_and_lvl3(False, query_switch, string, s1split))
            tot.append(max(res))
        elif "AND" in piece:
            tot.append(calculation_and_lvl3(True, query_switch, piece, s1split))
        else:
            tot.append(calculation_and_lvl3(False, query_switch, piece, s1split))
    return tot


def calculation_and_lvl1(first, second):
    if "!=" in first:
        s1split = first.split("!=", 1)[1]
        switch = 1
    elif "=" in first:  # elif "=" in first and "<" not in first:
        s1split = first.split("=", 1)[1]
        switch = 2
    elif ">" in first:
        s1split = first.split(">", 1)[1]
        s1split = s1split.replace(" ", "")
        switch = 3
    elif "<" in first:
        s1split = first.split("<>>", 1)[1]
        s1split = s1split.replace(" ", "")
        switch = 4
    else:
        return 0
    tot = calculation_and_lvl2(second, switch, s1split)
    return max(tot)



def f1a(string, s1split, s1attribute, matrix):
    if "!=" in string:
        s2attribute = string.split(" !=", 1)[0]
        string = string.split("!=", 1)[1]
        partial = fuzz.ratio(s1split, string)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def f1(string, s1split, s1attribute, matrix):
    string = string.split("AND", 1)
    for substring in string:
        matrix = f1a(substring, s1split, s1attribute, matrix)
    return matrix


def f77(string, s1split, s1attribute, matrix):
    string = string.split("AND", 1)
    for substring in string:
        matrix = f77a(substring, s1split, s1attribute, matrix)
    return matrix


def f77a(string, s1split, s1attribute, matrix):
    if "=" in string and "!=" not in string and "<" not in string:
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
                        matrix = f1(string, s1split, s1attribute, matrix)
                    else:
                        matrix = f1a(string, s1split, s1attribute, matrix)
            elif "AND" in piece:
                matrix = f1(piece, s1split, s1attribute, matrix)
            else:
                matrix = f1a(piece, s1split, s1attribute, matrix)
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
                            matrix = f77(string, s1split, s1attribute, matrix)
                        else:
                            matrix = f77a(string, s1split, s1attribute, matrix)
                elif "AND" in piece:
                    matrix = f77(piece, s1split, s1attribute, matrix)
                else:
                    matrix = f77a(piece, s1split, s1attribute, matrix)
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
                                    partial = 0
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
