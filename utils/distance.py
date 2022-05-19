from fuzzywuzzy import fuzz


def distance_calculator(string_1, string_2, distance_calculator_switch):
    if distance_calculator_switch == 1:
        return fuzz.ratio(string_1, string_2)
    """
    elif distance_calculator_switch == 2:
        return infersent
    """
