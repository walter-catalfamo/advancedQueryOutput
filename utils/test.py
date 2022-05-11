def selector(num):
    prefix = "data/"
    if num == 1:
        prefix += "Jodie/"
    elif num == 2:
        prefix += "Burt/"
    elif num == 3:
        prefix += "Ridley/"
    elif num == 4:
        prefix += "Movies/"
    source = prefix + "Source.csv"
    example = prefix + "Example.csv"
    target = prefix + "Target.csv"
    line = prefix + "Line.csv"
    return source, example, target, line


print(selector(3))
