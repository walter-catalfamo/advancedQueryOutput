from utils import query
from utils import decision_tree

def test_from_segment():
    assert query.from_segment(["city", "region"]) == "FROM city JOIN region "

def test_select_segment():
    assert query.select_segment(["cap", "size"]) == "SELECT cap, size "

def test_where_segment():
    table = [[1, 1900, 170], [1, 0, 120], [-1, 2000, 190], [-1, 2010, 120], [-1, 1650, 200]]

    clf = decision_tree.make_tree(table)

    joined_schema = ["I SHOULD NOT BE VISIBLE", "birth", "height"]

    assert query.where_segment(joined_schema, clf) == "WHERE ((birth <= 1950.0 AND ((birth <= 825.0) OR (birth > 825.0 AND ((birth > 1775.0))))))"
    
def test_decorate_tabe():
    joined_table = [[1900, 170, 10], [0, 120, 10], [0, 120, 100], [2010, 120, 10], [1650, 200, 10]]
    remove_columns = [2]
    example_table = [[1900, 170], [0, 120]]

    out = query.decorate_table(example_table, remove_columns, joined_table)

    assert out == [[1, 1900, 170, 10], [0, 0, 120, 10], [0, 0, 120, 100], [-1, 2010, 120, 10], [-1, 1650, 200, 10]], str(out)
    


