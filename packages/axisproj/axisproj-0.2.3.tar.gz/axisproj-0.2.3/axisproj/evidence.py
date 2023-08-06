from collections import defaultdict
from numpy.linalg import norm
from .utils import compute_CB


def compute_evidence(axis_aligned, X, projections, knn, eta=0.9):
    distortion = defaultdict(list)
    evidence = dict()

    cb = dict()
    max_e = 0
    d = X.shape[0]

    for ap in axis_aligned:
        alpha = ap['alpha']
        for idx in ap['LP']:
            if idx not in cb:
                Y = projections[idx].T.dot(X)
                cb[idx] = compute_CB(X, Y, knn)
            C, B = cb[idx]
            e = norm(C[:, alpha[0]] + C[:, alpha[1]] - B)
            distortion[alpha].append(e)
            max_e = max(max_e, e)

    total = 0
    for alpha, elist in distortion.items():
        mu = 1
        for e in elist:
            mu *= (1 - eta*(1-e/max_e))
        evidence[alpha] = 1 - mu
        total += 1 - mu

    for alpha in evidence.keys():
        evidence[alpha] /= total
    return evidence
