from src.topsis_model import topsis

def rank_machines(data, metrics, weights):

    matrix = data[metrics].values

    # convert dict weights to ordered list
    weight_vector = [weights[m] for m in metrics]

    scores = topsis(matrix, weight_vector)

    return scores