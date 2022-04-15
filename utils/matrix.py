import pandas as pd


def increase_matrix_element(first, second, per, matrix):
    # first = first.split("((",1)[1]
    # second = second.split(" ((",1)[1]
    first = first.replace(" ", "")
    second = second.replace(" ", "")
    row = 0
    col = 0
    for i in range(len(matrix.columns)):
        if matrix.columns[i] == second:
            col = i
    i = 0
    for i in range(len(matrix.index)):
        r = matrix.index[i].replace(" ", "")
        if r == first:
            row = i
    if row != 0 and col != 0:
        matrix.loc[matrix.index[row], matrix.columns[col]] += 1 * (per / 100)
    matrix.to_csv("data/matrix.csv", index_label=False)


def increase_matrix(first, second, per):
    increase_matrix_element(first, second, per, pd.read_csv("data/matrix.csv"))


def increase_new_matrix(first, second, per):
    increase_matrix_element(first, second, per, pd.read_csv("data/initial_matrix.csv"))
