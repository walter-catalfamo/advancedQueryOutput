import pandas as pd


def creator_iMatrix(source, target):
    path = source.split('/')  # path è un array formato da ogni parte della stringa 'source' separata da /
    right_folder = path[2]  # il folder è la terza posizione dell'array secondo l'attuale disposizione

    dfSource = pd.read_csv(source)
    dfTarget = pd.read_csv(target)

    index = []

    for y in dfSource.columns:
        index.append(y)

    columns = {}
    val = []

    for i in range(len(index)):
        val.append(0)

    for y in dfTarget.columns:
        columns.update({y: val})

    df = pd.DataFrame(columns, index)
    df.to_csv('../data/' + right_folder + '/initial_matrix.csv')


creator_iMatrix("../data/Population/Source.csv", "../data/Population/Target.csv")
