import utils.matrix
from utils import decision_tree, function
from utils import query
import pandas as pd
import csv
import itertools


def load_filename(file_name, output_file):
    """
    Loads a csv file and separates the attribute names from the actual rows
    :param file_name:
    :param output_file:
    :return:
    """
    db = pd.read_csv(file_name)
    db = pd.get_dummies(db, prefix_sep='*')
    db.to_csv(output_file, index=False)
    schema, data = load_schema(output_file)
    table = [[int(el) for el in row] for row in data[1:]]
    return schema, table


def load_schema(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    schema = [x.strip() for x in data[0]]
    return schema, data


def process(db_file, example_file, dbname):
    print()
    print("----------Loading: " + db_file + "," + example_file + " tables: " + str(dbname) + "----------")
    (db_schema, db_table) = load_filename(db_file, 'data/big.csv')
    (example_schema, example_table) = load_filename(example_file, 'data/enc.csv')
    print("------DB-------")
    print(db_schema)
    print("------EXAMPLE------")
    print(example_table)
    print(example_schema)
    missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
    annotated_table, ok = query.decorate_table(example_table, missing, db_table)
    if not ok:
        print("No query can be found to match a row in the example: ")
        return
    print("------DECORATED TABLE------")
    db_schema.insert(0, "I SHOULD NOT BE VISIBLE")
    gen_tree = decision_tree.make_tree(annotated_table)
    tree = []
    for node in gen_tree:
        tree.append(node)
    print("-------TREE-------")
    for node in tree:
        print(node)
    example_schema, _ = load_schema(example_file)
    queries = []
    for node in range(len(tree)):
        queries.append(query.tree_to_query(example_schema, dbname, db_schema, tree[node]))
    return queries


def query_creator(db_file, example_file):
    print()
    df = pd.read_csv(db_file)
    find, pppp = load_schema(example_file)
    final = []
    for y in find:
        found = []
        for x in df.columns:
            if y.isnumeric():
                if df[x].dtypes == 'int64':
                    if (df[x] == int(y)).any():
                        found.append(x)
            else:
                if (df[x] == y).any():
                    found.append(x)
        final.append(found)
    combination = []
    for element in itertools.product(*final):
        combination.append(element)
    print(combination)
    db_name = ["Rotten Tomatoes"]
    li = []
    for y in combination:
        ex = pd.DataFrame([find], columns=list(y))
        ex.to_csv("data/col.csv", index=False)
        s = process(db_file, "data/col.csv", db_name)
        li.append(s)
    return li


def select_source(num):
    example = ""
    if num == 1:
        example = "jodie/jodieSource.csv"
    elif num == 2:
        example = "burt/BurtReynoldsSource.csv"
    elif num == 3:
        example = "ridley/RidleySource.csv"
    return "sources/" + example


def select_example(num):
    example = ""
    if num == 1:
        example = "jodie/JodieExample.csv"
    elif num == 2:
        example = "burt/BurtExample.csv"
    elif num == 3:
        example = "ridley/RidleyExample.csv"
    return "sources/" + example


def select_target(num):  # Target
    example = ""
    if num == 1:
        example = "jodie/JodieTarget.csv"
    elif num == 2:
        example = "burt/BurtReynoldsTarget.csv"
    elif num == 3:
        example = "ridley/RidleyTarget.csv"
    return "sources/" + example


def select_line(num):  # Line
    example = ""
    if num == 1:
        example = "jodie/JodieLine.csv"
    elif num == 2:
        example = "burt/BurtLine.csv"
    elif num == 3:
        example = "ridley/RidleyLine.csv"
    return "sources/" + example


def filter_none(my_list):
    return [x for x in my_list if x is not None]


if __name__ == '__main__':
    matrix = pd.read_csv("data/initial_matrix.csv")
    table_names = ["imdb"]
    source_queries = process("data/jodieSource.csv", "data/JodieExample.csv", table_names)
    for string in source_queries:
        print(string)
    target_queries = query_creator("data/JodieTarget.csv", "data/JodieLine.csv")
    print(target_queries)
    target_queries = list(filter(None.__ne__, target_queries))
    s1 = []
    for i in range(len(source_queries)):
        s1.append(source_queries[i].split("WHERE ", 1)[1])
    s21 = []
    for i in range(len(target_queries)):
        s2 = []
        for string in target_queries[i]:
            s2.append(string.split("WHERE", 1)[1])
        s21.append(s2)
    finalLL = []

    """Confronto delle query chiamando la funzione calculationAnd presente nel file function.py"""
    for listSecondList in s21:
        totFirst = []
        for stringFirstList in s1:
            stringFirstList = stringFirstList.replace(")", "")
            if "OR" in stringFirstList:
                first = stringFirstList.split("OR", 1)
                resFirst = []
                for string in first:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partialFirst = []
                        for substring in string:
                            partialFirst.append(function.calculation_and_lvl1(substring, listSecondList))
                        resFirst.append(sum(partialFirst) / len(string))
                    else:
                        resFirst.append(function.calculation_and_lvl1(string, listSecondList))
                totFirst.append(max(resFirst))
            elif "AND" in stringFirstList:
                first = stringFirstList.split("AND", 1)
                partialFirst = []
                for string in first:
                    partialFirst.append(function.calculation_and_lvl1(string, listSecondList))
                totFirst.append(sum(partialFirst) / len(first))
            else:
                totFirst.append(function.calculation_and_lvl1(stringFirstList, listSecondList))
        print(totFirst)
        finalLL.append(totFirst)
    print(finalLL)
    valuesSorted = finalLL
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
        matrix = utils.matrix.increase_matrix(select1, select2, 500, matrix)
    else:
        matrix = utils.matrix.increase_matrix(select1.split(",", 1)[0], select2.split(",", 1)[0], 500, matrix)
        matrix = utils.matrix.increase_matrix(select1.split(",", 1)[1], select2.split(",", 1)[1], 500, matrix)
    for stringFirstList in s1:
        stringFirstList = stringFirstList.replace(")", "")
        if "OR" in stringFirstList:
            first = stringFirstList.split("OR", 1)
            for string in first:
                if "AND" in string:
                    string = string.split("AND", 1)
                    for substring in string:
                        matrix = function.find_attribute(substring, s21[indice], matrix)
                else:
                    matrix = function.find_attribute(string, s21[indice], matrix)
        elif "AND" in stringFirstList:
            first = stringFirstList.split("AND", 1)
            for string in first:
                matrix = function.find_attribute(string, s21[indice], matrix)
        else:
            matrix = function.find_attribute(stringFirstList, s21[indice], matrix)
    # matrix.to_csv("data/matrix.csv", index_label=False)
    print(matrix)
