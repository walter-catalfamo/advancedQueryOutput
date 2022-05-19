import pandas as pd
import csv
import itertools

from utils.calculator import find_attribute_lvl0, calculation_and_lvl0
from utils.classification import decision_tree
from utils.matrix import increase_matrix
from utils.query import decorate_table, tree_to_query


def query_from_decision_tree(annotated_table, example_schema, dbname, db_schema):
    queries = []
    gen_tree = decision_tree.make_tree(annotated_table)
    tree = []
    for node in gen_tree:
        tree.append(node)
    """
    print("-------TREE-------")
    for node in tree:
        print(node)
    """
    for node in range(len(tree)):
        queries.append(tree_to_query(example_schema, dbname, db_schema, tree[node]))
    return queries


def query_from_perceptron(db, example, dbname):
    queries = []
    return queries


def loadBig(file_name):
    """
    Loads a csv file and separates the attribute names from the actual rows
    :param file_name:
    :return:
    """
    # db = multiEncoding.encode(file_name)
    db = pd.read_csv(file_name)
    if ("newCountry" in db.columns):
        db = db.drop(["newLanguage", "newCountry"], axis=1)
    db = pd.get_dummies(db, prefix_sep='*')
    print(db)
    """I'm creating a csv file that will be read from the function after"""
    db.to_csv('big.csv', index=False)
    with open('big.csv', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
    schema = [x.strip() for x in data[0]]
    table = [[int(el) for el in row] for row in data[1:]]
    return schema, table


def load(file_name):
    """
    Loads a csv file and separates the attribute names from the actual rows
    :param file_name:
    :return:
    """
    # db = multiEncoding.encode(file_name)
    # otteniamo la stessa cosa utilizzando get_dummies, ho lasciato comunque implementato one_hot encoding di sklearn
    # ma non lo utilizzo

    db = pd.read_csv(file_name)
    db = pd.get_dummies(db, prefix_sep='*')
    """I'm creating a csv file that will be read from the function after"""

    db.to_csv('enc.csv', index=False)

    with open('enc.csv', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    schema = [x.strip() for x in data[0]]
    table = [[int(el) for el in row] for row in data[1:]]

    return schema, table


def load_test(file_name):
    """
    Loads a csv file and separates the attribute names from the actual rows
    :param file_name:
    :return:
    """
    # db = multiEncoding.encode(file_name)
    # otteniamo la stessa cosa utilizzando get_dummies, ho lasciato comunque implementato one_hot encoding di sklearn
    # ma non lo utilizzo

    db = pd.read_csv(file_name)
    db = pd.get_dummies(db, prefix_sep='*')
    """I'm creating a csv file that will be read from the function after"""

    db.to_csv('enc.csv', index=False)

    with open('enc.csv', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    schema = [x.strip() for x in data[0]]
    table = [[int(el) for el in row] for row in data[1:]]

    return schema, table


def query_producer2(db_file, example_file, dbname, classification_algorithm_switch):
    if classification_algorithm_switch == 1:
        (db_schema, db_table) = load_filename(db_file)
        # (db_schema, db_table) = loadBig(db_file)
        (example_schema, example_table) = load_filename(example_file)
        # (example_schema, example_table) = load(example_file)
        missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
        annotated_table = decorate_table(example_table, missing, db_table)
        db_schema.insert(0, "I SHOULD NOT BE VISIBLE")
        return query_from_decision_tree(annotated_table, example_schema, dbname, db_schema)
    elif classification_algorithm_switch == 2:
        db = pd.read_csv(db_file)
        example = pd.read_csv(example_file)
        return query_from_perceptron(db, example, dbname)


def load_filename(file_name):
    db = pd.read_csv(file_name)
    db = pd.get_dummies(db, prefix_sep='*')
    # db.to_csv(output_file, index=False)
    return read_db(db)


def read_row(row):
    partial = []
    for el in row:
        try:
            partial.append(int(el))
        except ValueError:
            if el == "":
                partial.append(0)
            else:
                partial.append(int(float(el)))
    return partial


def filter_nan(my_list):
    res = []
    for x in my_list:
        if str(x) != "nan":
            res.append(x)
        else:
            res.append(0)
    return res


def filter_multi_list_nan(my_list):
    res = []
    for x in my_list:
        res.append(filter_nan(x))
    return res


def read_db(db):
    schema = list(db.columns.values)
    # noinspection PyTypeChecker
    data = filter_multi_list_nan(db.to_numpy().tolist())
    return schema, data


def load_schema(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    schema = [x.strip() for x in data[0]]
    return schema


def process2(db_file, example_file, dbname, classification_algorithm_switch):
    return query_producer2(db_file, example_file, dbname, classification_algorithm_switch)


def filter_digit(multi_list):
    res = []
    for x in multi_list:
        if x[0].isdigit():
            res.append(int(x[0]))
        else:
            res.append(x[0])
    return [res]


def process_col(db_file, dbname, example_file, classification_algorithm_switch):
    return query_producer2(db_file, example_file, dbname, classification_algorithm_switch)


def loadExample(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    schema = [x.strip() for x in data[0]]
    return schema


def process_test(db_file, example_file, table_names):
    print()
    print("----------Loading: " + db_file + "," + example_file + " tables: " + str(table_names) + "----------")
    (db_schema, db_table) = loadBig(db_file)
    (example_schema, example_table) = load_test(example_file)

    print("------DB-------")
    print(db_schema)
    # print(db_table)

    print("------EXAMPLE------")
    print(example_table)
    print(example_schema)

    # finds which columns are to be projected away
    missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
    annotated_table = decorate_table(example_table, missing, db_table)

    print("------DECORATED TABLE------")
    # print(missing)
    # print(annotated_table)

    # print(db_schema)
    db_schema.insert(0, "I SHOULD NOT BE VISIBLE")

    # print(annotated_table)

    genTree = decision_tree.make_tree(annotated_table)
    tree = []
    for i in genTree:
        tree.append(i)

    print("-------TREE-------")

    for i in tree:
        print(i)
    """It is probably inefficient to load two times the example db but for now I don't have a better idea
    another idea could be to "calculate" the string names knowing that the two strings are separeted with _"""
    example_schema = loadExample(example_file)

    """In this other case I'm not going to load the df another time but I will study the columns name already encoded."""
    queries = []
    for i in range(len(tree)):
        queries.append(tree_to_query(example_schema, table_names, db_schema, tree[i]))
    return queries


def query_creator(db_file, example_file, classification_algorithm_switch):
    print()
    df = pd.read_csv(db_file)
    # find = load_schema(example_file)
    find = loadExample(example_file)
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
        ex.to_csv("data/col1.csv", index=False)
        # s = query_producer2(db_file, example_file, "data/col.csv", classification_algorithm_switch)
        s = process_test(db_file, "data/col1.csv", db_name)
        # s = process_col(db_file, db_name, ex)
        li.append(s)
    return li


def filter_none(my_list):
    return [x for x in my_list if x is not None]


def split_queries_source(sq):
    split_where_attributes_source = []
    for num_query in range(len(sq)):
        split_where_attributes_source.append(sq[num_query].split("WHERE ", 1)[1])
    return split_where_attributes_source


def split_queries_target(tq):
    split_where_attributes_target = []
    for i in range(len(tq)):
        temp_string = []
        for string in tq[i]:
            temp_string.append(string.split("WHERE", 1)[1])
        split_where_attributes_target.append(temp_string)
    return split_where_attributes_target


def build_similarity_matrix(select_source_attribute, select_target_attribute, split_source_queries, split_target_queries, maximum_value_position,
                            distance_calculator_switch):
    m = pd.read_csv("data/Burt/initial_matrix.csv")
    if "," not in select_source_attribute and "," not in select_target_attribute:
        m = increase_matrix(select_source_attribute, select_target_attribute, 500, m)
    else:
        m = increase_matrix(select_source_attribute.split(",", 1)[0], select_target_attribute.split(",", 1)[0], 500, m)
        m = increase_matrix(select_source_attribute.split(",", 1)[1], select_target_attribute.split(",", 1)[1], 500, m)
    m = find_attribute_lvl0(split_source_queries, split_target_queries, maximum_value_position, m, distance_calculator_switch)
    return m


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


def process(db_file, example_file, table_names):
    print()
    print("----------Loading: " + db_file + "," + example_file + " tables: " + str(table_names) + "----------")
    (db_schema, db_table) = loadBig(db_file)
    (example_schema, example_table) = load(example_file)

    print("------DB-------")
    print(db_schema)
    # print(db_table)

    print("------EXAMPLE------")
    print(example_table)
    print(example_schema)

    # finds which columns are to be projected away
    missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
    annotated_table, ok = decorate_table(example_table, missing, db_table)

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

    genTree = decision_tree.make_tree(annotated_table)
    tree = []
    for i in genTree:
        tree.append(i)

    print("-------TREE-------")

    for i in tree:
        print(i)
    """It is probably inefficient to load two times the example db but for now I don't have a better idea
    another idea could be to "calculate" the string names knowing that the two strings are separeted with _"""
    example_schema = loadExample(example_file)

    """In this other case I'm not going to load the df another time but I will study the columns name already encoded."""
    queries = []
    for i in range(len(tree)):
        queries.append(tree_to_query(example_schema, table_names, db_schema, tree[i]))
    return queries


def createExample(db_file, example_file):
    print()
    df = pd.read_csv(db_file)
    find = loadExample(example_file)
    found = []
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
        ex.to_csv("col.csv", index=False)
        s = process(db_file, "col.csv", table_names)
        li.append(s)
    return li


def run(selection, distance_calculator_switch, classification_algorithm_switch):
    table_names = ["myDB"]
    (source, example, target, line) = selector(selection)
    source_queries = query_producer2(source, example, table_names, classification_algorithm_switch)  # process
    # source_queries1 = process(source, example, table_names)
    for string in source_queries:
        print(string)
    target_queries = query_creator(target, line, classification_algorithm_switch)  # process
    # target_queries1 = createExample(target, line)
    print(target_queries)
    split_source_queries = split_queries_source(source_queries)
    split_target_queries = split_queries_target(target_queries)
    query_values = calculation_and_lvl0(split_target_queries, split_source_queries, distance_calculator_switch)
    print(query_values)
    query_values.sort()
    maximum_value_position = query_values.index(max(query_values))
    select_source_attribute = source_queries[0].split("FROM", 1)[0].split("SELECT", 1)[1]
    print(select_source_attribute)
    select_target_attribute = target_queries[maximum_value_position][0].split("FROM", 1)[0].split("SELECT", 1)[1]
    print(select_target_attribute)
    m = build_similarity_matrix(select_source_attribute, select_target_attribute, split_source_queries, split_target_queries,
                                maximum_value_position, distance_calculator_switch)
    # matrix.to_csv("data/matrix.csv", index_label=False)
    print(m)


def main():
    run(1, 1, 1)


main()
