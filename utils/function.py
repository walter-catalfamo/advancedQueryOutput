from fuzzywuzzy import fuzz

from utils.similarity_matrix import increase_matrix


def distance_calculator(string_1, string_2, distance_calculator_switch):
    if distance_calculator_switch == 1:
        return fuzz.ratio(string_1, string_2)
    """
    elif distance_calculator_switch == 2:
        return deep learning
    """


def calculation_and_lvl5_different(string, s1split, distance_calculator_switch):
    if "!=" in string:
        string = string.split("!=", 1)[1]
        return distance_calculator(s1split, string, distance_calculator_switch)
    else:
        return 0


def calculation_and_lvl5_equal(string, s1split, distance_calculator_switch):
    if "=" in string:
        string = string.split("=", 1)[1]
        return distance_calculator(s1split, string, distance_calculator_switch)
    else:
        return 0


def calculation_and_lvl5_greater(string, s1split, distance_calculator_switch):
    string = string.split(">", 1)[1]
    if float(s1split) < float(string):
        return 0
    else:
        return distance_calculator(s1split, string, distance_calculator_switch)


def calculation_and_lvl5_less(string, s1split, distance_calculator_switch):
    string = string.split("<", 1)[1]
    if float(s1split) < float(string):
        return distance_calculator(s1split, string, distance_calculator_switch)
    else:
        return 0


def calculation_and_lvl4(switch, string, s1split, distance_calculator_switch):
    if switch == 1:
        return calculation_and_lvl5_different(string, s1split, distance_calculator_switch)
    elif switch == 2:
        return calculation_and_lvl5_equal(string, s1split, distance_calculator_switch)
    elif switch == 3:
        return calculation_and_lvl5_greater(string, s1split, distance_calculator_switch)
    elif switch == 4:
        return calculation_and_lvl5_less(string, s1split, distance_calculator_switch)


def calculation_and_lvl3(loop_switch, query_switch, string, s1split, distance_calculator_switch):
    if loop_switch:
        string = string.split("AND", 1)
        res = []
        for substring in string:
            res.append(calculation_and_lvl4(query_switch, substring, s1split, distance_calculator_switch))
        return max(res)
    else:
        return calculation_and_lvl4(query_switch, string, s1split, distance_calculator_switch)


def calculation_and_lvl2(second, query_switch, s1split, distance_calculator_switch):
    tot = []
    for piece in second:
        piece = piece.replace("(", "").replace(")", "")
        if "OR" in piece:
            res = []
            s_or = piece.split("OR", 1)
            for string in s_or:
                if "AND" in string:
                    res.append(calculation_and_lvl3(True, query_switch, string, s1split, distance_calculator_switch))
                else:
                    res.append(calculation_and_lvl3(False, query_switch, string, s1split, distance_calculator_switch))
            tot.append(max(res))
        elif "AND" in piece:
            tot.append(calculation_and_lvl3(True, query_switch, piece, s1split, distance_calculator_switch))
        else:
            tot.append(calculation_and_lvl3(False, query_switch, piece, s1split, distance_calculator_switch))
    return tot


def calculation_and_lvl1(first, second, distance_calculator_switch):
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
        s1split = first.split("<", 1)[1].replace(" ", "")
        switch = 4
    else:
        return 0
    tot = calculation_and_lvl2(second, switch, s1split, distance_calculator_switch)
    return max(tot)


""""""""""""


def find_attribute_lvl5_different(string, s1split, s1attribute, matrix, distance_calculator_switch):
    if "!=" in string:
        s2attribute = string.split("!=", 1)[0]
        string = string.split("!=", 1)[1]
        partial = distance_calculator(s1split, string, distance_calculator_switch)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl5_equal(string, s1split, s1attribute, matrix, distance_calculator_switch):
    if "=" in string:
        s2attribute = string.split("=", 1)[0]
        string = string.split("=", 1)[1]
        partial = distance_calculator(s1split, string, distance_calculator_switch)
        matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl5_greater(string, s1split, s1attribute, matrix, distance_calculator_switch):
    s2attribute = string.split(">", 1)[0]
    string = string.split(">", 1)[1].replace(" ", "")
    if float(s1split) < float(string):
        partial = 0
    else:
        partial = distance_calculator(s1split, string, distance_calculator_switch)  # da verificare
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl5_less(string, s1split, s1attribute, matrix, distance_calculator_switch):
    s2attribute = string.split("<", 1)[0]
    string = string.split("<", 1)[1].replace(" ", "")
    if float(s1split) < float(string):
        partial = distance_calculator(s1split, string, distance_calculator_switch)  # da verificare
    else:
        partial = 0
    matrix = increase_matrix(s1attribute, s2attribute, partial, matrix)
    return matrix


def find_attribute_lvl4(query_switch, string, s1split, s1attribute, matrix, distance_calculator_switch):
    if query_switch == 1:
        return find_attribute_lvl5_different(string, s1split, s1attribute, matrix, distance_calculator_switch)
    elif query_switch == 2:
        return find_attribute_lvl5_equal(string, s1split, s1attribute, matrix, distance_calculator_switch)
    elif query_switch == 3:
        return find_attribute_lvl5_greater(string, s1split, s1attribute, matrix, distance_calculator_switch)
    elif query_switch == 4:
        return find_attribute_lvl5_less(string, s1split, s1attribute, matrix, distance_calculator_switch)


def find_attribute_lvl3(loop_switch, query_switch, string, s1split, s1attribute, matrix, distance_calculator_switch):
    if loop_switch:
        string = string.split("AND", 1)
        for substring in string:
            matrix = find_attribute_lvl4(query_switch, substring, s1split, s1attribute, matrix, distance_calculator_switch)
    else:
        matrix = find_attribute_lvl4(query_switch, string, s1split, s1attribute, matrix, distance_calculator_switch)
    return matrix


def find_attribute_lvl2(second, s1attribute, query_switch, s1split, matrix, distance_calculator_switch):
    for piece in second:
        piece = piece.replace("(", "").replace(")", "")
        if "OR" in piece:
            s_or = piece.split("OR", 1)
            for string in s_or:
                if "AND" in string:
                    matrix = find_attribute_lvl3(True, query_switch, string, s1split, s1attribute, matrix, distance_calculator_switch)
                else:
                    matrix = find_attribute_lvl3(False, query_switch, string, s1split, s1attribute, matrix, distance_calculator_switch)
        elif "AND" in piece:
            matrix = find_attribute_lvl3(True, query_switch, piece, s1split, s1attribute, matrix, distance_calculator_switch)
        else:
            matrix = find_attribute_lvl3(False, query_switch, piece, s1split, s1attribute, matrix, distance_calculator_switch)
    return matrix


def find_attribute_lvl1(first, second, matrix, distance_calculator_switch):
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
    matrix = find_attribute_lvl2(second, s1attribute, switch, s1split, matrix, distance_calculator_switch)
    return matrix
