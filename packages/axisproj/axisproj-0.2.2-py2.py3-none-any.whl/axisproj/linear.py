import numpy as np
import nudged
from scipy.linalg import eig, sqrtm, norm

from .utils import adjust


def find_linear_projections(X, d, objective, iters=20):
    n = X.shape[1]
    objective.X = X

    XBXT = adjust(objective.XBXT)
    sqrtXBXT = np.real(sqrtm(XBXT))

    projections = []
    selected = []
    C = np.zeros((X.shape[0], X.shape[0]))

    for i in range(iters):
        if i == 0:
            XLXT = objective.XLXT
        else:
            XLXT = objective.XLXT + objective.alpha * C
            XLXT = 0.5 * (XLXT + XLXT.T)
        XLXT = adjust(XLXT)
        ev, eV, *_ = eig(XLXT, XBXT)

        ev = np.real(ev)
        eV = np.dot(sqrtXBXT, np.real(eV))

        if objective.alpha < 0:
            ev = -ev
        idx = np.argsort(ev)
        V = eV[:, idx[0:d]]

        for j in range(d):
            V[:, j] /= norm(V[:, j])

        projections.append(V)
        C += V.dot(V.T)

        if i == 0 or dissimilar(V, selected, X, objective.threshold):
            selected.append(V)
    return selected


def dissimilar(V, projections, X, min_threshold, err_threshold=0.8):
    VT = V.T
    m = 2 - min(map(lambda p: norm(VT.dot(p)), projections))
    if m < min_threshold:
        return False

    Y = X.T.dot(V).tolist()
    for p in projections:
        Y2 = X.T.dot(p)
        affine = nudged.estimate(Y, Y2.tolist())
        err = norm(Y2 - np.array(affine.transform(Y))) / norm(Y2)
        if err < err_threshold:
            return False
    return True



