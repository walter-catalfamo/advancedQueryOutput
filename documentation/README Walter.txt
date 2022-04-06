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
    make_tree(annotated_table):
        purity_kind(annotated_table)

    purity_kind(table):
        if all rows have the same annotations, then return it
        otherwise return 0

