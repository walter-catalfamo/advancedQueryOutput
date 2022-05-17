import pandas as pd
import csv
import itertools

from utils import query, decision_tree
from utils.function import find_attribute_caller, match
from utils.matrix import increase_matrix


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


def load_filename(file_name):
    db = pd.read_csv(file_name)
    db = pd.get_dummies(db, prefix_sep='*')
    # db.to_csv(output_file, index=False)
    return read_db(db)


def load_schema(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    schema = [x.strip() for x in data[0]]
    return schema


def query_producer(db_schema, example_table, example_schema, db_table, dbname):
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
    """"""

    gen_tree = decision_tree.make_tree(annotated_table)
    tree = []
    for node in gen_tree:
        tree.append(node)
    print("-------TREE-------")

    for node in tree:
        print(node)
    queries = []
    """"""

    for node in range(len(tree)):
        queries.append(query.tree_to_query(example_schema, dbname, db_schema, tree[node]))
    return queries


def process(db_file, example_file, dbname):
    (db_schema, db_table) = load_filename(db_file)
    (example_schema, example_table) = load_filename(example_file)
    return query_producer(db_schema, example_table, example_schema, db_table, dbname)


def filter_digit(multi_list):
    res = []
    for x in multi_list:
        if x[0].isdigit():
            res.append(int(x[0]))
        else:
            res.append(x[0])
    return [res]


def process_col(db_file, dbname, ex):
    (db_schema, db_table) = load_filename(db_file)
    # (example_schema, example_table) = load_filename(example_file)
    (example_schema, example_table) = read_db(ex)
    example_table = filter_digit(example_table)
    return query_producer(db_schema, example_table, example_schema, db_table, dbname)


def process_col2(db_file, dbname, example_file):
    (db_schema, db_table) = load_filename(db_file)
    (example_schema, example_table) = load_filename(example_file)
    return query_producer(db_schema, example_table, example_schema, db_table, dbname)


def query_creator(db_file, example_file):
    print()
    df = pd.read_csv(db_file)
    find = load_schema(example_file)
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
        s = process_col2(db_file, db_name, "data/col.csv")
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


def build_similarity_matrix(select_source_attribute, select_target_attribute, split_source_queries,
                            split_target_queries, maximum_value_position, distance_calculator_switch):
    m = pd.read_csv("data/Burt/initial_matrix.csv")
    if "," not in select_source_attribute and "," not in select_target_attribute:
        m = increase_matrix(select_source_attribute, select_target_attribute, 500, m)
    else:
        m = increase_matrix(select_source_attribute.split(",", 1)[0],
                            select_target_attribute.split(",", 1)[0], 500, m)
        m = increase_matrix(select_source_attribute.split(",", 1)[1],
                            select_target_attribute.split(",", 1)[1], 500, m)
    m = find_attribute_caller(split_source_queries, split_target_queries, maximum_value_position, m, distance_calculator_switch)
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


def main():
    selection = 1
    distance_calculator_switch = 1
    table_names = ["myDB"]
    (source, example, target, line) = selector(selection)
    source_queries = process(source, example, table_names)
    for string in source_queries:
        print(string)
    target_queries = filter_none(query_creator(target, line))
    print(target_queries)
    split_source_queries = split_queries_source(source_queries)
    split_target_queries = split_queries_target(target_queries)
    query_values = match(split_target_queries, split_source_queries, distance_calculator_switch)
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


main()
