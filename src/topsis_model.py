import numpy as np

def topsis(matrix, weights):

    matrix = np.array(matrix, dtype=float)
    weights = np.array(weights, dtype=float)

    denom = np.sqrt((matrix**2).sum(axis=0))

    denom[denom == 0] = 1   # avoid divide by zero

    norm = matrix / denom

    weighted = norm * weights

    ideal_best = weighted.max(axis=0)
    ideal_worst = weighted.min(axis=0)

    dist_best = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    return score