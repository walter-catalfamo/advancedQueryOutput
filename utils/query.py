from utils import decision_tree


def from_segment(tables):
    """
    Builds the from part of the query
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
    # input_schema = multiEncoding.inverse(input_schema)ù
    # I'm finding difficult to find a way to reverse encode the database as I have constructed it
    # I'm thinking we could call a function loadExample that will pass as input_schema the initial example db.
    return "SELECT " + ", ".join(input_schema) + " "


def tree_to_where(joined_schema, tree):
    """
    Recursively builds the logic formula representing the given decision tree
    :param joined_schema: list of attributes in the joined schema
    :param tree: the Tree built
    :return: a condition on the attributes of the joined schema and a value representing if there is at least one path to a positive leaf
    """
    if not isinstance(tree, decision_tree.Tree):  # if this is a leaf, return True if it is a positive one, false else
        if tree == 1:
            return "", True
        return "FALSE", False

    # extract the attribute considered in the root node
    attribute_name = joined_schema[tree.attributeColumn]

    # build the logical formulae of the left and right subtree
    (lquery, lres) = tree_to_where(joined_schema, tree.left)
    (rquery, rres) = tree_to_where(joined_schema, tree.right)

    if lquery != "":  # if the left subtree is not a leaf , prepare to build attribute_name<=threshold AND ...
        lquery = " AND " + lquery

    if rquery != "":  # if the right subtree is not a leaf  , prepare to build attribute_name>threshold AND ...
        rquery = " AND " + rquery

    # if both left and right subtrees don't have any path to a positive leaf, return false as this subtree is useless
    if not lres and not rres:
        return "FALSE", False

    squery = "("

    if lres:  # if the left subtree is relevant ( has a path to a positive leaf) add it
        if ('*' in attribute_name):
            index = attribute_name.find('*')
            copy = attribute_name[0:index]
            second = attribute_name[index + 1:]
            squery = squery + "(" + copy + " != " + second
            squery = squery + lquery + ")"
        else:
            squery = squery + "(" + attribute_name + " <= " + str(tree.threshold)
            squery = squery + lquery + ")"

        # squery = ( (attribute_name <= threshold AND left_subtree_condition)

    if lres and rres:  # if both subtrees are relevant add an OR condition
        squery = squery + " OR "

    if rres:  # if the right subtree is relevant
        if ('*' in attribute_name):
            index = attribute_name.find('*')
            copy = attribute_name[0:index]
            second = attribute_name[index + 1:]
            squery = squery + "(" + copy + " = " + second
            squery = squery + rquery + ")"
        else:
            squery = squery + "(" + attribute_name + " > " + str(tree.threshold)
            squery = squery + rquery + ")"

        # squery +=  (attribute_name > threshold AND right_subtree_condition)
    squery = squery + ")"

    return squery, True


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


def projected_table(missing, joined_table):
    """
    Projects a table by removing some columns on a copy
    :param missing: column indexes to be removed
    :param joined_table: the table to pe projected
    :return: the projected table
    """
    cloned_table = []
    for row in joined_table:
        y = row
        cloned_table.append(row.copy())
        for column in reversed(missing):
            """reversed to avoid segmentation faults"""
            del cloned_table[-1][column]
    return cloned_table


def differentiate_tables(cloned_table, example_table):
    kinds = [-1] * len(cloned_table)
    for row in example_table:
        ls = []  # indexes that project to this row
        for (index, join_row) in enumerate(cloned_table):
            if join_row == row:
                ls.append(index)
        if not ls:  # if an example row doesn't match any projection, the query is impossible
            return row, False
        for index in ls:
            kinds[index] = 1 if len(ls) == 1 else 0  # set all indexes to 0, or 1 if there is only one
    return kinds


def decorate_table(example_table, missing, joined_table):
    """
    Takes a table and decorates it by adding a leading column with the selected class for each row
    The values are -1, if the row doesn't project to a row in the example table (bound negative)
    0 if the row does project to a row in the example table, but it isn't the only one (free)
    1 if the row does project to a row in the example table and it is the only one (bound positive)
    Returns a row of the example if a row in the example isn't obtainable
    :param example_table: the example table from the user
    :param missing: the columns to be removed from the output
    :param joined_table: the joined table from the database
    :return: the joined table decorated with a leading column or the empty list and a boolean indicating success
    """

    # project all rows
    cloned_table = projected_table(missing, joined_table)
    print("------PROJECTED TABLE & TARGET CLASSES-------")
    print(cloned_table)
    kinds = differentiate_tables(cloned_table, example_table)
    print("kinds: ")
    print(kinds)
    # adds the kind column at the beginning of the joined table
    for (row, kind) in zip(joined_table, kinds):
        row.insert(0, kind)
    return joined_table, True
