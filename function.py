from fuzzywuzzy import fuzz
import matrix


def f1(string, s1split):
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
    return max(partial)


def f3(string, s1split):
    if "<" in string:
        string = string.split("=", 1)[1]
        string = string.replace(" ", "")
        if float(s1split) < float(string):
            return 100
        else:
            return 0
    elif ">" in string:
        string = string.split(">", 1)[1]
        string = string.replace(" ", "")
        if float(s1split) < float(string):
            return 0
        else:
            return 100
    else:
        return 0


def f5(string, s1split, s1attribute):
    string = string.split("AND", 1)
    for substring in string:
        if "!=" in substring:
            s2attribute = substring.split(" !=", 1)[0]
            substring = substring.split("!=", 1)[1]
            partial = fuzz.ratio(s1split, substring)
            matrix.increase_matrix(s1attribute, s2attribute, partial)


def f6_ciclo(string, s1split, s1attribute):
    string = string.split("AND", 1)
    for substring in string:
        if "=" in substring:
            if "!=" not in substring and "<" not in substring:
                s2attribute = substring.split(" =", 1)[0]
                substring = substring.split("=", 1)[1]
                partial = fuzz.ratio(s1split, substring)
                matrix.increase_matrix(s1attribute, s2attribute, partial)


def f9a_ciclo(string, s1split, s1attribute):
    string = string.split("AND", 1)
    for substring in string:
        if "<" in substring:
            s2attribute = substring.split("<", 1)[0]
            substring = substring.split("<", 1)[1]
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
                partial = 0
            else:
                partial = 100
            matrix.increase_matrix(s1attribute, s2attribute, partial)


def f10(second, s1split, s1attribute):
    elimina_parentesi(second)
    for piece in second:
        piece = elimina_parentesi(piece)
        if "OR" in piece:
            temp_string = piece.split("OR", 1)
            for string in temp_string:
                f9a_ciclo(string, s1split, s1attribute)
        else:
            f9a_ciclo(piece, s1split, s1attribute)


def elimina_parentesi(string):
    string = string.replace("(", "")
    string = string.replace(")", "")
    return string


def calculation_and(first, second):
    tot = []
    if "!=" in first:
        attribute_value = first.split("!=", 1)[1]
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                res = []
                temp_string = piece.split("OR", 1)
                for string in temp_string:
                    if "AND" in string:
                        res.append(f1(string, attribute_value))
                    else:
                        if "!=" in string:
                            string = string.split("!=", 1)[1]
                            res.append(fuzz.ratio(attribute_value, string))
                        else:
                            res.append(0)
                tot.append(max(res))
            elif "AND" in piece:
                tot.append(f1(piece, attribute_value))
            else:
                if "!=" in piece:
                    string = piece.split("!=", 1)[1]
                    tot.append(fuzz.ratio(attribute_value, string))
                else:
                    tot.append(0)
        return max(tot)
    elif "=" in first:
        if "<" not in first:
            attribute_value = first.split("=", 1)[1]
            for piece in second:
                piece = piece.replace(")", "")
                if "OR" in piece:
                    res = []
                    temp_string = piece.split("OR", 1)
                    for string in temp_string:
                        res.append(f1(string, attribute_value))
                    tot.append(max(res))
                else:
                    tot.append(f1(piece, attribute_value))
            return max(tot)
        else:
            attribute_value = first.split("=", 1)[1]
            attribute_value = attribute_value.replace(" ", "")
            for piece in second:
                piece = piece.replace(")", "")
                if "OR" in piece:
                    res = []
                    temp_string = piece.split("OR", 1)
                    for string in temp_string:
                        if "AND" in string:
                            string = string.split("AND", 1)
                            partial = []
                            for substring in string:
                                if "<" in substring:
                                    substring = substring.split("=", 1)[1]
                                    substring = substring.replace(" ", "")
                                    if float(attribute_value) <= float(substring):
                                        partial.append(100)
                                    else:
                                        partial.append(100)  # da decidere
                                elif ">" in substring:
                                    substring = substring.split(">", 1)[1]
                                    substring = substring.replace(" ", "")
                                    if float(attribute_value) < float(substring):
                                        partial.append(0)  # niente intersezione
                                    else:
                                        partial.append(100)  # intersezione
                                else:
                                    partial.append(0)  # nel target non ho un valore numerico
                            res.append(max(partial))
                        else:
                            res.append(f3(string, attribute_value))
                    tot.append(max(res))
                elif "AND" in piece:
                    string = piece.split("AND", 1)
                    partial = []
                    for substring in string:
                        partial.append(f3(substring, attribute_value))
                    tot.append(max(partial))
                else:
                    tot.append(f3(piece, attribute_value))
            return max(tot)
    else:
        attribute_value = first.split(">", 1)[1]
        attribute_value = attribute_value.replace(" ", "")
        for piece in second:
            piece = piece.replace(")", "")
            if "OR" in piece:
                res = []
                temp_string = piece.split("OR", 1)
                for string in temp_string:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partial = []
                        for substring in string:
                            partial.append(f3(substring, attribute_value))
                        res.append(max(partial))
                    else:
                        res.append(f3(string, attribute_value))
                tot.append(max(res))
            elif "AND" in piece:
                string = piece.split("AND", 1)
                partial = []
                for substring in string:
                    partial.append(f3(substring, attribute_value))
                tot.append(max(partial))
            else:
                if "<" in piece:
                    string = piece.split("=", 1)[1]
                    string = string.replace(" ", "")
                    if float(attribute_value) < float(string):
                        tot.append(100)
                    else:
                        tot.append(0)
                elif ">" in piece:
                    string = piece.split(">", 1)[1]
                    string = string.replace(" ", "")
                    if float(attribute_value) < float(string):
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
            piece = elimina_parentesi(piece)
            if "OR" in piece:
                temp_string = piece.split("OR", 1)
                for string in temp_string:
                    if "AND" in string:
                        f5(string, s1split, s1attribute)

            else:
                f5(piece, s1split, s1attribute)
    elif "=" in first:
        if "<" not in first:
            s1split = first.split("=", 1)[1]
            s1attribute = first.split("=", 1)[0]
            for piece in second:
                piece = elimina_parentesi(piece)
                if "OR" in piece:
                    temp_string = piece.split("OR", 1)
                    for string in temp_string:
                        f6_ciclo(string, s1split, s1attribute)
                elif "AND" in piece:
                    f6_ciclo(piece, s1split, s1attribute)
        else:
            s1split = first.split("=", 1)[1]
            s1split = s1split.replace(" ", "")
            s1attribute = first.split("<", 1)[0]
            f10(second, s1split, s1attribute)
    else:
        s1split = first.split(">", 1)[1]
        s1split = s1split.replace(" ", "")
        s1attribute = first.split(">", 1)[0]
        f10(second, s1split, s1attribute)
