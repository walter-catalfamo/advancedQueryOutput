from utils import decision_tree
from utils import query
from utils import function
from utils import matrix
import pandas as pd
import csv
import itertools

write_enable = False


def load(file_name, output_file):
    """
    Loads a csv file and separates the attribute names from the actual rows
    """
    # db = multiEncoding.encode(file_name)
    db = pd.read_csv(file_name)
    """
    if ("newCountry" in db.columns):
        db = db.drop(["newLanguage", "newCountry"], axis=1)
    """
    db = pd.get_dummies(db, prefix_sep='*')
    print(db)
    """I'm creating a csv file that will be read from the function after"""
    if write_enable:
        db.to_csv(output_file, index=False)
    with open(output_file, newline='', encoding="utf-8") as f:
        data = list(csv.reader(f))
    schema = [x.strip() for x in data[0]]
    table = [[int(el) for el in row] for row in data[1:]]
    return schema, table


def load_file(file_name):
    with open(file_name, newline='') as f:
        data = list(csv.reader(f))
    schema = [x.strip() for x in data[0]]
    return schema


def process(db_file, example_file, table_names):
    print()
    print("----------Loading: " + db_file + "," + example_file + " tables: " + str(table_names) + "----------")
    (db_schema, db_table) = load(db_file, "data/big.csv")
    (example_schema, example_table) = load(example_file, "data/enc.csv")
    print("------DB-------")
    print(db_schema)
    # print(db_table)
    print("------EXAMPLE------")
    print(example_table)
    print(example_schema)
    # finds which columns are to be projected away
    missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
    annotated_table, ok = query.decorate_table(example_table, missing, db_table)
    if not ok:
        print("No query can be found to match a row in the example: ")
        # print(str(annotated_table))
        return
    print("------DECORATED TABLE------")
    # print(missing)
    # print(annotated_table)
    # print(db_schema)
    db_schema.insert(0, "I SHOULD NOT BE VISIBLE")
    # print(annotated_table)
    gen_tree = decision_tree.make_tree(annotated_table)
    tree = []
    for node in gen_tree:
        tree.append(node)
    print("-------TREE-------")
    for node in tree:
        print(node)
    """
    It is probably inefficient to load two times the example db but for now I don't have a better idea
    another idea could be to "calculate" the string names knowing that the two strings are separated with _
    """
    example_schema = load_file(example_file)
    """
    In this other case I'm not going to load the df another time but I will study the columns name already encoded.
    """
    queries = []
    for node in range(len(tree)):
        queries.append(query.tree_to_query(example_schema, table_names, db_schema, tree[node]))
    return queries


def query_creator(db_file, example_file):
    print()
    df = pd.read_csv(db_file)
    find = load_file(example_file)
    final = []
    for string in find:
        found = []
        for x in df.columns:
            if string.isnumeric():
                if df[x].dtypes == 'int64':
                    if (df[x] == int(string)).any():
                        found.append(x)
            else:
                if (df[x] == string).any():
                    found.append(x)
        final.append(found)

    combination = []
    for element in itertools.product(*final):
        combination.append(element)
    print(combination)
    table_names = ["Rotten Tomatoes"]
    li = []
    for string in combination:
        ex = pd.DataFrame([find], columns=list(string))
        if write_enable:
            ex.to_csv("data/col.csv", index=False)
        s = process(db_file, "data/col.csv", table_names)
        li.append(s)
    return li


def select_source(num):
    if num == 1:
        example = "jodie/jodieSource.csv"
    elif num == 2:
        example = "burt/BurtReynoldsSource.csv"
    elif num == 3:
        example = "ridley/RidleySource.csv"
    return "sources/" + example


def select_example(num):
    if num == 1:
        example = "jodie/JodieExample.csv"
    elif num == 2:
        example = "burt/BurtExample.csv"
    elif num == 3:
        example = "ridley/RidleyExample.csv"
    return "sources/" + example


def select_target(num): # Target
    if num == 1:
        example = "jodie/JodieTarget.csv"
    elif num == 2:
        example = "burt/BurtReynoldsTarget.csv"
    elif num == 3:
        example = "ridley/RidleyTarget.csv"
    return "sources/" + example


def select_line(num): # Line
    if num == 1:
        example = "jodie/JodieLine.csv"
    elif num == 2:
        example = "burt/BurtLine.csv"
    elif num == 3:
        example = "ridley/RidleyLine.csv"
    return "sources/" + example


def filter_none(l):
    return [x for x in l if x is not None]


if __name__ == '__main__':
    table_names = ["imdb"]
    selection = 2
    source_queries = process(select_source(selection), select_example(selection), table_names)
    for string in source_queries:
        print(string)
    target_queries = filter_none(query_creator(select_target(selection), select_line(selection)))
    print(target_queries)

    SPLITTED_QUERIES_SOURCE = []
    for i in range(len(source_queries)):
        SPLITTED_QUERIES_SOURCE.append(source_queries[i].split("WHERE ", 1)[1])
    SPLITTED_QUERIES_TARGET = []
    for i in range(len(target_queries)):
        temp_string = []
        for string in target_queries[i]:
            temp_string.append(string.split("WHERE", 1)[1])
        SPLITTED_QUERIES_TARGET.append(temp_string)

    final_list = []

    for listSecondList in SPLITTED_QUERIES_TARGET:
        totFirst = []
        for stringFirstList in SPLITTED_QUERIES_SOURCE:
            stringFirstList = stringFirstList.replace(")", "")
            if "OR" in stringFirstList:
                first = stringFirstList.split("OR", 1)
                resFirst = []
                for string in first:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partialFirst = []
                        for substring in string:
                            partialFirst.append(function.calculation_and(substring, listSecondList))
                        resFirst.append(sum(partialFirst) / len(string))
                    else:
                        resFirst.append(function.calculation_and(string, listSecondList))
                totFirst.append(max(resFirst))
            elif "AND" in stringFirstList:
                first = stringFirstList.split("AND", 1)
                partialFirst = []
                for string in first:
                    partialFirst.append(function.calculation_and(string, listSecondList))
                totFirst.append(sum(partialFirst) / len(first))
            else:
                totFirst.append(function.calculation_and(stringFirstList, listSecondList))
        print(totFirst)
        final_list.append(totFirst)
    print(final_list)
    valuesSorted = final_list
    for string in valuesSorted:
        string.sort(reverse=True)
    massimo = valuesSorted[0][0]
    indice = 0
    i = 1
    while i < len(valuesSorted):
        val = valuesSorted[i][0]
        if val > massimo:
            massimo = val
            indice = i
        elif val == massimo:
            if valuesSorted[i][1] > valuesSorted[indice][1]:
                indice = i
            elif valuesSorted[i][1] == valuesSorted[indice][1]:
                if valuesSorted[i][2] > valuesSorted[indice][2]:
                    indice = i
        i = i + 1
    print(valuesSorted)
    print(indice)
    select1 = source_queries[0].split("FROM", 1)[0]
    select1 = select1.split("SELECT", 1)[1]
    select2 = target_queries[indice][0].split("FROM", 1)[0]
    select2 = select2.split("SELECT", 1)[1]
    if "," not in select1 and "," not in select2:
        print(select1)
        print(select2)
        matrix.increase_new_matrix(select1, select2, 500)
    else:
        matrix.increase_matrix(select1.split(",", 1)[0], select2.split(",", 1)[0], 500)
        matrix.increase_matrix(select1.split(",", 1)[1], select2.split(",", 1)[1], 500)
    for stringFirstList in SPLITTED_QUERIES_SOURCE:
        stringFirstList = stringFirstList.replace(")", "")
        if "OR" in stringFirstList:
            first = stringFirstList.split("OR", 1)
            for string in first:
                if "AND" in string:
                    string = string.split("AND", 1)
                    for substring in string:
                        function.find_attribute(substring, SPLITTED_QUERIES_TARGET[indice])
                else:
                    function.find_attribute(string, SPLITTED_QUERIES_TARGET[indice])
        elif "AND" in stringFirstList:
            first = stringFirstList.split("AND", 1)
            for string in first:
                function.find_attribute(string, SPLITTED_QUERIES_TARGET[indice])
        else:
            function.find_attribute(stringFirstList, SPLITTED_QUERIES_TARGET[indice])
    matrix = pd.read_csv("data/matrix.csv")
    print(matrix)

"""
    # fin = process("ClooneySource.csv", "TonyExample.csv", table_names)
    fin = process(source, "sources/jodie/JodieExample.csv", table_names)
    # fin = process("angeEthanSource2.csv","2014example.csv", table_names)
    # fin = process("angeEthanSource2.csv","MusicExample.csv", table_names)
    # fin = process("angeEthanSource2.csv","AngelinaExample.csv", table_names)
    # fin = process("angeEthanSource2.csv","137Angelina.csv", table_names)
    # fin = process("sources/burt/BurtReynoldsSource.csv", "sources/burt/BurtExample.csv", table_names)
    # fin = process("sources/ridley/RidleySource.csv", "sources/ridley/RidleyExample.csv", table_names)
    # fin = process ("126Source.csv","126Example.csv",table_names)

    # pro = query_creator("ClooneyTarget.csv","TonyLine.csv")
    pro = query_creator("sources/jodie/JodieTarget.csv", "sources/jodie/JodieLine.csv")
    # pro = query_creator("angeEthanTarget.csv","2014line.csv")
    # pro = query_creator("angeEthanTarget.csv","MusicLine.csv")
    # pro = query_creator("angeEthanTarget.csv","AngelinaLine.csv") #ci impiega tanto, 270 secondi
    # pro = query_creator("angeEthanTarget.csv","137line.csv")
    # pro = query_creator("sources/burt/BurtReynoldsTarget.csv", "sources/burt/BurtLine.csv")
    # pro = query_creator("sources/ridley/RidleyTarget.csv", "sources/ridley/RidleyLine.csv")
    # pro = query_creator("126Target.csv","126Line.csv")
"""
