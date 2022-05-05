from fuzzywuzzy import fuzz

from utils.similarity_matrix import increase_matrix


def distance_calculator(s1split, string, distance_calculator_switch):
    if distance_calculator_switch == 1:
        return fuzz.ratio(s1split, string)
    """
    elif distance_calculator_switch == 2:
        return deep learning
    """


def calculation_and_lvl5_different(string, s1split):
    if "!=" in string:
        string = string.split("!=", 1)[1]
        return fuzz.ratio(s1split, string)
    else:
        return 0


def calculation_and_lvl5_equal(string, s1split):
    if "=" in string:
        string = string.split("=", 1)[1]
        return fuzz.ratio(s1split, string)
    else:
        return 0


def calculation_and_lvl5_greater(string, s1split):
    string = string.split(">", 1)[1]
    if float(s1split) < float(string):
        return 0
    else:
        return 100


def calculation_and_lvl5_less(string, s1split):
    string = string.split("<", 1)[1]
    if float(s1split) < float(string):
        return 100
    else:
        return 0


def calculation_and_lvl4(switch, string, s1split):
    if switch == 1:
        return calculation_and_lvl5_different(string, s1split)
    elif switch == 2:
        return calculation_and_lvl5_equal(string, s1split)
    elif switch == 3:
        return calculation_and_lvl5_greater(string, s1split)
    elif switch == 4:
        return calculation_and_lvl5_less(string, s1split)


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
        piece = piece.replace("(", "").replace(")", "")
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
    first = first.replace("(", "").replace(")", "")
    if "!=" in first:
        s1split = first.split("!=", 1)[1].replace(" ", "")
        switch = 1
    elif "=" in first:
        s1split = first.split("=", 1)[1].replace(" ", "")
        switch = 2
    elif ">" in first:
        s1split = first.split(">", 1)[1].replace(" ", "")
        switch = 3
    elif "<" in first:
        s1split = first.split("<>>", 1)[1].replace(" ", "")
        switch = 4
    else:
        return 0
    tot = calculation_and_lvl2(second, switch, s1split)
    return max(tot)


def find_attribute_lvl5_different(string, s1split, s1attribute, matrix):
    if "!=" in string:
        s2attribute = string.split("!=", 1)[0]
        string = string.split("!=", 1)[1]
        partial = fuzz.ratio(s1split, string)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl5_equal(string, s1split, s1attribute, matrix):
    if "=" in string:
        s2attribute = string.split("=", 1)[0]
        string = string.split("=", 1)[1]
        partial = fuzz.ratio(s1split, string)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl5_greater(string, s1split, s1attribute, matrix):
    s2attribute = string.split(">", 1)[0]
    string = string.split(">", 1)[1].replace(" ", "")
    if float(s1split) < float(string):
        partial = 0
    else:
        partial = 100 * fuzz.ratio(s1split, string)  # da verificare
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl5_less(string, s1split, s1attribute, matrix):
    s2attribute = string.split("<", 1)[0]
    string = string.split("<", 1)[1].replace(" ", "")
    if float(s1split) < float(string):
        partial = 100 * fuzz.ratio(s1split, string)  # da verificare
    else:
        partial = 0
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl4(query_switch, string, s1split, s1attribute, matrix):
    if query_switch == 1:
        return find_attribute_lvl5_different(string, s1split, s1attribute, matrix)
    elif query_switch == 2:
        return find_attribute_lvl5_equal(string, s1split, s1attribute, matrix)
    elif query_switch == 3:
        return find_attribute_lvl5_greater(string, s1split, s1attribute, matrix)
    elif query_switch == 4:
        return find_attribute_lvl5_less(string, s1split, s1attribute, matrix)


def find_attribute_lvl3(loop_switch, query_switch, string, s1split, s1attribute, matrix):
    if loop_switch:
        string = string.split("AND", 1)
        for substring in string:
            matrix = find_attribute_lvl4(query_switch, substring, s1split, s1attribute, matrix)
    else:
        matrix = find_attribute_lvl4(query_switch, string, s1split, s1attribute, matrix)
    return matrix


def find_attribute_lvl2(second, s1attribute, query_switch, s1split, matrix):
    for piece in second:
        piece = piece.replace("(", "").replace(")", "")
        if "OR" in piece:
            s_or = piece.split("OR", 1)
            for string in s_or:
                if "AND" in string:
                    matrix = find_attribute_lvl3(True, query_switch, string, s1split, s1attribute, matrix)
                else:
                    matrix = find_attribute_lvl3(False, query_switch, string, s1split, s1attribute, matrix)
        elif "AND" in piece:
            matrix = find_attribute_lvl3(True, query_switch, piece, s1split, s1attribute, matrix)
        else:
            matrix = find_attribute_lvl3(False, query_switch, piece, s1split, s1attribute, matrix)
    return matrix


def find_attribute_lvl1(first, second, matrix):
    first = first.replace("(", "").replace(")", "")
    if "!=" in first:
        s1split = first.split("!=", 1)[1]
        s1attribute = first.split("!=", 1)[0]
        switch = 1
    elif "=" in first:
        s1split = first.split("=", 1)[1]
        s1attribute = first.split("=", 1)[0]
        switch = 2
    elif ">" in first:
        s1split = first.split(">", 1)[1]
        s1attribute = first.split(">", 1)[0]
        switch = 3
    elif "<" in first:
        s1split = first.split("<", 1)[1]
        s1attribute = first.split("<", 1)[0]
        switch = 4
    else:
        return matrix
    matrix = find_attribute_lvl2(second, s1attribute, switch, s1split, matrix)
    return matrix
