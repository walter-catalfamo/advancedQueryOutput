from fuzzywuzzy import fuzz

from utils.similarity_matrix import increase_matrix


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
        piece = piece.replace("(", "")
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
    first = first.replace("(", "")
    first = first.replace(")", "")
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







def find_attribute_f1(string, s1split, s1attribute, matrix):
    if "!=" in string:
        s2attribute = string.split("!=", 1)[0]
        string = string.split("!=", 1)[1]
        partial = fuzz.ratio(s1split, string)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_f2(string, s1split, s1attribute, matrix):
    if "=" in string:
        s2attribute = string.split("=", 1)[0]
        string = string.split("=", 1)[1]
        partial = fuzz.ratio(s1split, string)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_f3(string, s1split, s1attribute, matrix):
    s2attribute = string.split(">", 1)[0]
    string = string.split(">", 1)[1]
    string = string.replace(" ", "")
    if float(s1split) < float(string):
        partial = 0
    else:
        partial = 100
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_f4(string, s1split, s1attribute, matrix):
    s2attribute = string.split("<", 1)[0]
    string = string.split("<", 1)[1]
    string = string.replace(" ", "")
    if float(s1split) < float(string):
        partial = 100
    else:
        partial = 0
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl4(query_switch, string, s1split, s1attribute, matrix):
    if query_switch == 1:
        return find_attribute_f1(string, s1split, s1attribute, matrix)
    elif query_switch == 2:
        return find_attribute_f2(string, s1split, s1attribute, matrix)
    elif query_switch == 3:
        return find_attribute_f3(string, s1split, s1attribute, matrix)
    elif query_switch == 4:
        return find_attribute_f4(string, s1split, s1attribute, matrix)


def find_attribute_lvl3(loop_switch, query_switch, string, s1split, s1attribute, matrix):
    if loop_switch:
        string = string.split("AND", 1)
        for substring in string:
            matrix = find_attribute_lvl4(query_switch, substring, s1split, s1attribute, matrix)
    else:
        matrix = find_attribute_lvl4(query_switch, string, s1split, s1attribute, matrix)
    return matrix


def find_attribute_lvl2(second, query_switch, s1split, matrix):
    for piece in second:
        piece = piece.replace("(", "")
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


def find_attribute_lvl1(first, second, matrix):
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
                                matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                    else:
                        if "!=" in string:
                            s2attribute = string.split(" !=", 1)[0]
                            string = string.split("!=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
            elif "AND" in piece:
                string = piece.split("AND", 1)
                for substring in string:
                    if "!=" in substring:
                        s2attribute = substring.split(" !=", 1)[0]
                        substring = substring.split("!=", 1)[1]
                        partial = fuzz.ratio(s1split, substring)
                        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
            else:
                if "!=" in piece:
                    s2attribute = string.split(" !=", 1)[0]
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
                            string = string.split("AND", 1)
                            for substring in string:
                                if "=" in substring:
                                    if "!=" not in substring and "<" not in substring:
                                        s2attribute = substring.split(" =", 1)[0]
                                        substring = substring.split("=", 1)[1]
                                        partial = fuzz.ratio(s1split, substring)
                                        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                        else:
                            if "=" in string:
                                if "!=" not in string and "<" not in string:
                                    s2attribute = string.split(" =", 1)[0]
                                    string = string.split("=", 1)[1]
                                    partial = fuzz.ratio(s1split, string)
                                    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    for substring in string:
                        if "=" in substring:
                            if "!=" not in substring and "<" not in substring:
                                s2attribute = substring.split(" =", 1)[0]
                                substring = substring.split("=", 1)[1]
                                partial = fuzz.ratio(s1split, substring)
                                matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                else:
                    if "=" in piece:
                        if "!=" not in piece and "<" not in piece:
                            s2attribute = piece.split(" =", 1)[0]
                            string = piece.split("=", 1)[1]
                            partial = fuzz.ratio(s1split, string)
                            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
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
                                    s2attribute = substring.split(">", 1)[0]
                                    substring = substring.split(">", 1)[1]
                                    substring = substring.replace(" ", "")
                                    if float(s1split) < float(substring):
                                        partial = 0  # niente intersezione
                                    else:
                                        partial = 100  # intersezione
                                    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                        else:
                            if "<" in string:
                                s2attribute = string.split("<", 1)[0]
                                string = string.split("=", 1)[1]
                                string = string.replace(" ", "")
                                if float(s1split) < float(string):
                                    partial = 100
                                else:
                                    partial = 0
                                matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
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
                            s2attribute = substring.split("<", 1)[0]
                            substring = substring.split("=", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial = 100
                            else:
                                partial = 0
                            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                        elif ">" in substring:
                            s2attribute = substring.split(">", 1)[0]
                            substring = substring.split(">", 1)[1]
                            substring = substring.replace(" ", "")
                            if float(s1split) < float(substring):
                                partial = 0  # in questo caso i due intervalli non hanno intersezioni
                            else:
                                partial = 100
                            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                else:
                    if "<" in piece:
                        s2attribute = piece.split("<", 1)[0]
                        string = piece.split("=", 1)[1]
                        string = string.replace(" ", "")
                        if float(s1split) < float(string):
                            partial = 100
                        else:
                            partial = 0
                        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
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
                                matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                            elif ">" in substring:
                                s2attribute = substring.split(" >", 1)[0]
                                substring = substring.split(">", 1)[1]
                                substring = substring.replace(" ", "")
                                if float(s1split) < float(substring):
                                    partial = 100
                                else:
                                    partial = 100
                                matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                    else:
                        if "<" in string:
                            s2attribute = string.split(" <", 1)[0]
                            string = string.split("=", 1)[1]
                            string = string.replace(" ", "")
                            if float(s1split) < float(string):
                                partial = 100
                            else:
                                partial = 0
                            matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                        elif ">" in string:  # se nel target ho > invece di <=
                            s2attribute = string.split(" >", 1)[0]
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
                        s2attribute = substring.split(" <", 1)[0]
                        substring = substring.split("=", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial = 100
                        else:
                            partial = 0
                        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
                    elif ">" in substring:
                        s2attribute = substring.split(" >", 1)[0]
                        substring = substring.split(">", 1)[1]
                        substring = substring.replace(" ", "")
                        if float(s1split) < float(substring):
                            partial = 100
                        else:
                            partial = 100
                        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
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
                    s2attribute = piece.split(" >", 1)[0]
                    string = piece.split(">", 1)[1]
                    string = string.replace(" ", "")
                    if float(s1split) < float(string):
                        partial = 100
                    else:
                        partial = 100
                    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix
