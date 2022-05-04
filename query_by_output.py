from utils import decision_tree, function, similarity_matrix, query
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
        example = "data/Movies/imdbSource.csv"
    elif num == 2:
        example = "data/Jodie/jodieSource.csv"
    elif num == 3:
        example = "ridley/RidleySource.csv"
    return example


def select_example(num):
    example = ""
    if num == 1:
        example = "data/Movies/movieExample.csv"
    elif num == 2:
        example = "data/Jodie/JodieExample.csv"
    elif num == 3:
        example = "ridley/RidleyExample.csv"
    return example


def select_target(num):  # Target
    example = ""
    if num == 1:
        example = "data/Movies/imdb_top_1000Target.csv"
    elif num == 2:
        example = "data/Jodie/JodieTarget.csv"
    elif num == 3:
        example = "ridley/RidleyTarget.csv"
    return example


def select_line(num):  # Line
    example = ""
    if num == 1:
        example = "data/Movies/movieLine.csv"
    elif num == 2:
        example = "data/Jodie/JodieLine.csv"
    elif num == 3:
        example = "ridley/RidleyLine.csv"
    return example


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


def match(tq, sq):
    qv = []
    for attribute_found_target in tq:
        match_points = []
        for attribute_found_source in sq:
            attribute_found_source = attribute_found_source.replace(")", "")
            if "OR" in attribute_found_source:
                first_part = attribute_found_source.split("OR", 1)
                point = []
                for string in first_part:
                    if "AND" in string:
                        string = string.split("AND", 1)
                        partial_point = []
                        for substring in string:
                            partial_point.append(function.calculation_and_lvl1(substring, attribute_found_target))
                        point.append(sum(partial_point) / len(string))
                    else:
                        point.append(function.calculation_and_lvl1(string, attribute_found_target))
                match_points.append(max(point))
            elif "AND" in attribute_found_source:
                first_part = attribute_found_source.split("AND", 1)
                partial_point = []
                for string in first_part:
                    partial_point.append(function.calculation_and_lvl1(string, attribute_found_target))
                match_points.append(sum(partial_point) / len(first_part))
            else:
                match_points.append(function.calculation_and_lvl1(attribute_found_source, attribute_found_target))
        print(match_points)
        qv.append(match_points)
    return qv


def find_attribute_caller(split_source_queries, split_target_queries, maximum_value_position, matrix):
    for attribute_found_source in split_source_queries:
        attribute_found_source = attribute_found_source.replace(")", "").replace(")", "")
        if "OR" in attribute_found_source:
            first_part = attribute_found_source.split("OR", 1)
            for string in first_part:
                if "AND" in string:
                    string = string.split("AND", 1)
                    for substring in string:
                        matrix = function.find_attribute_lvl1(substring, split_target_queries[maximum_value_position], matrix)
                else:
                    matrix = function.find_attribute_lvl1(string, split_target_queries[maximum_value_position], matrix)
        elif "AND" in attribute_found_source:
            first_part = attribute_found_source.split("AND", 1)
            for string in first_part:
                matrix = function.find_attribute_lvl1(string, split_target_queries[maximum_value_position], matrix)
        else:
            matrix = function.find_attribute_lvl1(attribute_found_source, split_target_queries[maximum_value_position], matrix)
    return matrix


def build_similarity_matrix(select_source_attribute, select_target_attribute, split_source_queries, split_target_queries, maximum_value_position):
    matrix = pd.read_csv("data/initial_matrix.csv")
    if "," not in select_source_attribute and "," not in select_target_attribute:
        matrix = similarity_matrix.increase_matrix(select_source_attribute, select_target_attribute, 500, matrix)
    else:
        matrix = similarity_matrix.increase_matrix(select_source_attribute.split(",", 1)[0], select_target_attribute.split(",", 1)[0], 500, matrix)
        matrix = similarity_matrix.increase_matrix(select_source_attribute.split(",", 1)[1], select_target_attribute.split(",", 1)[1], 500, matrix)
    matrix = find_attribute_caller(split_source_queries, split_target_queries, maximum_value_position, matrix)
    return matrix


def main():
    table_names = ["imdb"]
    selection = 2
    source_queries = process(select_source(selection), select_example(selection), table_names)
    for string in source_queries:
        print(string)
    target_queries = filter_none(query_creator(select_target(selection), select_line(selection)))
    print(target_queries)
    split_source_queries = split_queries_source(source_queries)
    split_target_queries = split_queries_target(target_queries)
    query_values = match(split_target_queries, split_source_queries)
    print(query_values)
    query_values.sort()
    maximum_value_position = query_values.index(max(query_values))
    select_source_attribute = source_queries[0].split("FROM", 1)[0].split("SELECT", 1)[1]
    print(select_source_attribute)
    select_target_attribute = target_queries[maximum_value_position][0].split("FROM", 1)[0].split("SELECT", 1)[1]
    print(select_target_attribute)
    matrix = build_similarity_matrix(select_source_attribute, select_target_attribute, split_source_queries, split_target_queries,
                                     maximum_value_position)
    # matrix.to_csv("data/matrix.csv", index_label=False)
    print(matrix)


main()
