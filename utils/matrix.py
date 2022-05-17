import pandas as pd


def matrix_creator(source, target):
    path = source.split('/')  # path è un array formato da ogni parte della stringa 'source' separata da /
    right_folder = path[2]  # il folder è la terza posizione dell'array secondo l'attuale disposizione
    df_source = pd.read_csv(source)
    df_target = pd.read_csv(target)
    index = []
    for y in df_source.columns:
        index.append(y)
    columns = {}
    val = []
    for i in range(len(index)):
        val.append(0)
    for y in df_target.columns:
        columns.update({y: val})
    df = pd.DataFrame(columns, index)
    df.to_csv('../data/' + right_folder + '/initial_matrix.csv')


def create_matrix():
    matrix_creator("../data/Population/Source.csv", "../data/Population/Target.csv")


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
