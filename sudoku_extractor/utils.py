import numpy as np


def get_distance(p1, p2):
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]

    return np.sqrt((d1 ** 2 + d2 ** 2))
