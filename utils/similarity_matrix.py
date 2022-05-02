def increase_matrix(first, second, per, matrix):
    first = first.replace(" ", "")
    second = second.replace(" ", "")
    row = 0
    col = 0
    for i in range(len(matrix.columns)):
        if matrix.columns[i] == second:
            col = i
    for i in range(len(matrix.index)):
        r = matrix.index[i].replace(" ", "")
        if r == first:
            row = i
    matrix.loc[matrix.index[row], matrix.columns[col]] += 1 * (per / 100)
    return matrix
