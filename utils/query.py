from utils.classification import decision_tree


def from_segment(tables):
    """
    Builds the FROM part of the query
    :param tables: a list of table names
    :return: "From table1 join table2 join ...
    """
    return "FROM " + " JOIN ".join(tables) + " "


def select_segment(input_schema):
    """
    Builds the select part of the query
    :param input_schema: the columns of the joined schema to select
    :return: Select attr1, attr2,...
    """
    if type(input_schema) is list:
        return "SELECT " + input_schema[0].split("*")[0] + " "
    else:
        return "SELECT " + input_schema.split("*")[0] + " "


def tree_to_where(joined_schema, tree):
    """
    Recursively builds the logic formula representing the given decision tree
    :param joined_schema: list of attributes in the joined schema
    :param tree: the Tree built
    :return: a condition on the attributes of the joined schema and a value representing if
    there is at least one path to a positive leaf
    """
    if not isinstance(tree, decision_tree.Tree):  # if this is a leaf, return True if it is a positive one, false else
        if tree == 1:
            return "", True
        return "FALSE", False
    attribute_name = joined_schema[tree.attributeColumn]
    (l_query, l_res) = tree_to_where(joined_schema, tree.left)
    (r_query, r_res) = tree_to_where(joined_schema, tree.right)
    if l_query != "":  # if the left subtree is not a leaf , prepare to build attribute_name<=threshold AND ...
        l_query = " AND " + l_query
    if r_query != "":  # if the right subtree is not a leaf  , prepare to build attribute_name>threshold AND ...
        r_query = " AND " + r_query
    if not l_res and not r_res:
        return "FALSE", False
    s_query = "("
    if l_res:  # if the left subtree is relevant ( has a path to a positive leaf) add it
        if '*' in attribute_name:
            index = attribute_name.find('*')
            copy = attribute_name[0:index]
            second = attribute_name[index + 1:]
            s_query = s_query + "(" + copy + " != " + second
            s_query = s_query + l_query + ")"
        else:
            s_query = s_query + "(" + attribute_name + " <= " + str(tree.threshold)
            s_query = s_query + l_query + ")"
    if l_res and r_res:  # if both subtrees are relevant add an OR condition
        s_query = s_query + " OR "
    if r_res:  # if the right subtree is relevant
        if '*' in attribute_name:
            index = attribute_name.find('*')
            copy = attribute_name[0:index]
            second = attribute_name[index + 1:]
            s_query = s_query + "(" + copy + " = " + second
            s_query = s_query + r_query + ")"
        else:
            s_query = s_query + "(" + attribute_name + " > " + str(tree.threshold)
            s_query = s_query + r_query + ")"
    s_query = s_query + ")"
    return s_query, True


def where_segment(joined_schema, tree):
    """
    Builds the where segment of the query
    :param joined_schema: list of attributes in the joined schema
    :param tree: the Tree built
    :return: where attr...
    """
    return "WHERE " + tree_to_where(joined_schema, tree)[0]


def tree_to_query(input_schema, tables, joined_schema, tree):
    """
    Generate a SQL query from a decision tree
    :param input_schema: the schema of the example table
    :param tables: the name of the tables to be joined
    :param joined_schema: the schema of the joined table
    :param tree: the Tree
    :return: the SQL query
    """

    select = select_segment(input_schema)
    frm = from_segment(tables)
    where = where_segment(joined_schema, tree)

    return select + frm + where


def projected_table(remove_columns, joined_table):
    """
    Projects a table by removing some columns on a copy
    :param remove_columns: column indexes to be removed
    :param joined_table: the table to pe projected
    :return: the projected table
    """
    cloned_table = []
    for row in joined_table:
        cloned_table.append(row.copy())
        for column in reversed(remove_columns):
            del cloned_table[-1][column]

    return cloned_table


def decorate_table(example_table, remove_columns, joined_table):
    """
    Takes a table and decorates it by adding a leading column with the selected class for each row
    The values are -1, if the row doesn't project to a row in the example table (bound negative)
    0 if the row does project to a row in the example table, but it isn't the only one (free)
    1 if the row does project to a row in the example table, and it is the only one (bound positive)
    Returns a row of the example if a row in the example isn't obtainable
    :param example_table: the example table from the user
    :param remove_columns: the columns to be removed from the output
    :param joined_table: the joined table from the database
    :return: the joined table decorated with a leading column or the empty list and a boolean indicating success
    """

    kinds = [-1] * len(joined_table)

    cloned_table = projected_table(remove_columns, joined_table)
    print("------PROJECTED TABLE & TARGET CLASSES-------")
    print(cloned_table)

    for row in example_table:
        ls = []  # indexes that project to this row
        for (index, join_row) in enumerate(cloned_table):
            if join_row == row:
                ls.append(index)
        if not ls:  # if an example row doesn't match any projection, the query is impossible
            return row
        for index in ls:
            kinds[index] = 1 if len(ls) == 1 else 0  # set all indexes to 0, or 1 if there is only one

    print(kinds)

    for (row, kind) in zip(joined_table, kinds):
        row.insert(0, kind)

    return joined_table
