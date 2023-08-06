import numpy as np
from sklearn.neighbors import kneighbors_graph


def precision_recall(X, Y, n, factor):
    T = Y.shape[1]
    G = kneighbors_graph(X.T, n, mode='connectivity', include_self=False).toarray()
    H = kneighbors_graph(Y.T, int(n*factor), mode='connectivity', include_self=False).toarray()

    TP = np.multiply(G,H).sum(axis=1)
    FP = np.multiply((1-G),H).sum(axis=1)
    FN = np.multiply(G,(1-H)).sum(axis=1)

    p = np.divide(TP,TP+FP)
    r = np.divide(TP,TP+FN)

    return (p + r)/2


def histogram(qfactor=1.0, qsize=30, bins=10, range=(0.0, 1.0)):
    def f(V, X):
        Y = V.T.dot(X)
        pr = precision_recall(X, Y, qsize, qfactor)
        hist = np.histogram(pr, bins, range=range)
        return hist[0].tolist()
    return f