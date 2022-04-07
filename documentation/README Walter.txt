QUERY_BY_OUTPUT
    main():
        process(source, example, imdb) -> return queries
    process(db_file, example_file, table_names):
        load(db_file) -> (db_schema, db_table)
        load(example_file) -> (example_schema, example_table)
        missing = list of attributes in db_schema that are not in example_schema  
        query.decorate_table(example_table, missing, db_table) -> (annotated_table, ok)
        genTree = decision_tree.make_tree(annotated_table)
    load(file_name): //used to read source file
        read file_name.csv
        get_dummies
        schema = list of possible values (Attribute name * Value)
        table = for each row 1 if the value is that one, 0 otherwise
        return (schema, table)

QUERY
    query.decorate_table(example_table, missing, joined_table):
        cloned_table = projected_table(missing, joined_table)
        kinds = differentiate_tables(cloned_table, example_table)
        zip(kinds, joined_table)
    projected_table(missing, joined_table):
        create cloned_table
        joined_table without the columns that are missing
    differentiate_tables(cloned_table, example_table):
        kinds = [-1 ...] -> length = |joined_table|
        if the element is present but it is not the only one -> kinds[i] = 0
        if the element is present and it is the only one -> kinds[i] = 1

DECISION_TREE
    make_tree(table):
        purity_kind(table)
        gen = attribute_score(table)
        left =
        right = 
        threshold =
        gini =
        attribute_column =

    purity_kind(table):
        if all rows have the same annotations, then return it
        otherwise return 0
    attribute_score(table):
        for attr in range(1, len(table[0])):
            (left, right, threshold, gini) = divide(table, attr)
            yield left, right, threshold, gini, attr
    divide(table, attribute_column):
        threshold, gini = find_threshold(table, attribute_column)
    
    def find_threshold(table, attribute_column):
        use sklearn libraries to return threshold, gini
            threshold is set as 0.5 by default and should not change for binary classification problems
        gini_index is a measure of how often a randomly chosen element from the set would be incorrectly labeled if it was randomly labeled according to the distribution of labels in the subset.
