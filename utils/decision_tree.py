from sklearn import tree
from heapq import nsmallest


def find_threshold(table, attribute_column):
    """
    Given a decorated table and a column index to use, returns the optimal threshold to use and its gini value
    :param table: the decorated table( table[0] contains the target of each row)
    :param attribute_column: the column to use
    :return: pair threshold,gini
    """
    # use sklearn's decision tree to find the best split value
    clf = tree.DecisionTreeClassifier()
    dataset = ([x[attribute_column]] for x in table)
    target = (x[0] for x in table)
    clf = clf.fit(list(dataset), list(target))
    """threshold = clf.tree_.threshold[0].item()"""
    threshold = 0.5
    gini = clf.tree_.impurity[0].item()
    return gini


def divide(table, attribute_column):
    """
    Given a decorated table and a column index to use, splits the table according to the optimal threshold
    :param table: the decorated table
    :param attribute_column: the column to uyse
    :return: a decorated table containing the rows with row[attributeColumn]<=threshold, a table with the other rows, the
            threshold and the gini value
    """
    threshold = 0.5
    left = [x for x in table if x[attribute_column] <= threshold]
    right = [x for x in table if x[attribute_column] > threshold]
    # if not left or not right:  # if left or right are empty this split should be discarded
    if len(left) == 0 or len(right) == 0:
        gini = 999
    else:
        gini = split_gini(left, right) * find_threshold(table, attribute_column)
    return left, right, threshold, gini


def count_of_class(table, cls):
    """
    Returns the value of the fraction of rows that pertain to cls
    :param table: a decorated table
    :param cls: class to use
    :return: fraction of rows pertaining to class cls
    """
    return sum(1.0 if x[0] == cls else 0.0 for x in table) / len(table)


def single_gini(s):
    """
    Calculates the gini value of a single decorated table considering 3 classes
    :param s: set to use
    :return: gini value
    """
    unass = count_of_class(s, 0)
    pos = count_of_class(s, 1)
    neg = count_of_class(s, -1)
    gini = 1.0 - ((unass * unass) + (pos * pos) + (neg * neg))
    assert gini >= 0.0
    # print("pos is "+str(pos)+" neg is "+str(neg)+" unass is "+str(unass)+" gini "+str(gini))
    return gini


def split_gini(s1, s2):
    """
    Calculates the gini value of two decorated tables considering 3 classes
    :param s1: first table
    :param s2: second table
    :return: gini value
    """
    return (len(s1) * single_gini(s1)) + (len(s2) * single_gini(s2)) / (len(s1) + len(s2))


def attribute_score(table):
    """
    Calculates the score of each attribute and yields the split tables and gini value
    :param table: table to be split
    """
    for attr in range(1, len(table[0])):
        (left, right, threshold, gini) = divide(table, attr)
        yield left, right, threshold, gini, attr


def purity_kind(table):
    """
    Checks if a table is pure (all rows are of the same class)
    :param table: the decorated table
    :return: 1 if all rows are bound positive, -1 if all are bound negative, 0 else
    """
    assert len(table) != 0
    same_kind = list((x for x in table if x[0] == table[0][0]))
    if len(same_kind) == len(table):
        return table[0][0]
    return 0


def child_to_string(child, nesting):
    """
    To string method for a child
    :param child:  child to be serialized
    :param nesting: nesting level
    :return: a string representation of a child
    """
    return child.recursiveStr(nesting) if isinstance(child, Tree) else ("\t" * nesting) + str(child)


class Tree:
    def __init__(self, left, right, threshold, attributeColumn):
        self.left = left
        self.right = right
        self.threshold = threshold
        self.attributeColumn = attributeColumn

    def recursiveStr(self, nesting):
        """
        Builds a string representation of the tree
        :param nesting: nesting value
        :return: a tree in the form
        attribute: index_of attribute threshold threshold_value
        /left_child
        /right_child
        """
        me = "attribute: " + str(self.attributeColumn) + " threshold " + str(self.threshold)

        left_str = child_to_string(self.left, nesting + 1)
        right_str = child_to_string(self.right, nesting + 1)

        return ("\t" * nesting) + me + "\n" + left_str + "\n" + right_str

    def __str__(self):
        return self.recursiveStr(0)


def update_free(table, new_value):
    """
    Changes in place all free tuples to the new value
    :param table: decorated table
    :param new_value: new value
    """
    for row in table:
        if row[0] == 0:
            row[0] = new_value


def make_tree(table):
    """
    Recursive function that given a decorated table build a decision tree on it using case C1 of the paper
    :param table: table to be analyzed
    :return: the Tree built
    """
    if not table:  # if table is empty
        return -1
    kind = purity_kind(table)  # find out if the table is pure, if it is then this leaf node is ok, return
    if kind != 0:
        yield kind
        return
    gen = attribute_score(table)
    """In questo modo sto creando una lista per ogni variabile e ogni elemento della lista corrisponde ad un albero 
    di un attributo specifico."""
    left = []
    right = []
    threshold = []
    gini = []
    attribute_column = []
    for i in gen:
        left.append(i[0])
        right.append(i[1])
        threshold.append(i[2])
        gini.append(i[3])
        attribute_column.append(i[4])
    # case C1 puts as positive all free tuples
    for i in range(len(left)):
        update_free(left[i], 1)
        update_free(right[i], 1)
    # build left and right subtrees
    """"seleziono solo i 3 alberi con il gini migliore su tutti gli split possibili e continuo a dividere l'albero solo 
    da questi."""
    num = nsmallest(3, gini)  # ["0,0","999"]
    index = []
    for i in range(len(num)):
        #   if num[i] != 999:
        index.append(gini.index(num[i]))
        gini[gini.index(
            num[i])] = 'a'  # nel caso avessi duplicati cambio il gini appena considerato per ottere il giusto indice
    for i in index:
        if left[i] != [] and right[i] != []:
            # print(left[i])
            left[i] = list(make_tree(left[i]))[0]
            right[i] = list(make_tree(right[i]))[0]
    for i in index:
        yield Tree(left[i], right[i], threshold[i], attribute_column[i])
