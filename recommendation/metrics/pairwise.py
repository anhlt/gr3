import numpy as np
import scipy.spatial.distance as ssd

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('metrics')


def euclidean_distances(X, Y, squared=False, inveser=True):
    if X is Y:
        X = Y = np.asanyarray(X)
    else:
        X = np.asanyarray(X)
        Y = np.asanyarray(Y)

    if X.shape[1] != Y.shape[1]:
        raise ValueError("Incompatible dimension for X and Y matrices")

    if squared:
        return ssd.cdist(X, Y, 'sqeuclidean')
    XY = ssd.cdist(X, Y)
    result = np.divide(1.0, (1.0 + XY)) if inveser else XY

    return result


def cosine_distances(X, Y):
    if X is Y:
        X = Y = np.asanyarray(X)
    else:
        X = np.asanyarray(X)
        Y = np.asanyarray(Y)

    if X.shape[1] != Y.shape[1]:
        raise ValueError("Incompatible dimension for X and Y matrices")

    return 1. - ssd.cdist(X, Y, 'cosine')

    XY = ssd.cdist(X, Y)
    result = np.divide(1.0, (1.0 + XY)) if inveser else XY

    return result


def disagreement_variance(X):
    return np.square(X - X.mean(0)).mean(0)
	

