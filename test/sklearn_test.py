from sklearn import tree
from utils import decision_tree


def test_simple_tree():
    X = [[0], [1]]
    Y = [0, 1]
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    assert clf.predict([[0.]])[0] == 0
    assert clf.predict([[1.]])[0] == 1
    assert clf.tree_.threshold[0] == 0.5


def test_simple_tree_equal_classes():
    X = [[0], [1]]
    Y = [0, 0]
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    assert clf.predict([[0.]])[0] == 0
    assert clf.predict([[1.]])[0] == 0


def test_find_treshold():
    table = [[1, "asdasd", 100], [-1, "asd", 0]]
    assert decision_tree.find_threshold(table, 2)[0] == 50
    assert decision_tree.find_threshold(table, 2)[0] != 20


def test_divide():
    table = [[1, "a", 100], [-1, "b", 0]]
    (left, right, threshold, gini) = decision_tree.divide(table, 2)
    assert right[0] == table[0]
    assert left[0] == table[1]
    assert threshold == 50


def test_purity_kind():
    table = [[1, "asdasd", 100], [-1, "asd", 0]]
    assert decision_tree.purity_kind(table) == 0
    table = [[1, "asdasd", 100], [1, "asd", 0]]
    assert decision_tree.purity_kind(table) == 1


def test_query_tree():
    table = [[1, 1900, 170], [1, 0, 120], [-1, 2000, 190], [-1, 2010, 120], [-1, 1650, 200]]

    clf = decision_tree.make_tree(table)
    assert clf.threshold == 1950
