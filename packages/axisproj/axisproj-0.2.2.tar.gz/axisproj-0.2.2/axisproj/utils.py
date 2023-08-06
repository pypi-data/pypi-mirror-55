import numpy as np
from numpy.linalg import norm, eig
from sklearn.neighbors import kneighbors_graph


def adjust(M):
    v, *_ = eig(M)
    mv = np.min(np.real(v))
    if mv < 0:
        M = M - mv * np.eye(M.shape[0])
    return M


def compute_CB(X, Y, knn):
    G = kneighbors_graph(Y.T, knn, mode='connectivity', include_self=False).toarray()
    G = np.maximum(G, G.T)

    qi, qj = np.where(np.triu(G == 1))
    C = np.power(X[:, qi] - X[:, qj], 2).T
    C[np.isinf(C)] = 0
    C[np.isnan(C)] = 0

    dy = Y[:, qi] - Y[:, qj]
    B = np.power(norm(dy, axis=0).reshape(dy.shape[1], 1), 2)
    return C, B


def make_basis(d, alpha):
    Z = np.zeros((d, 2))
    Z[alpha[0], 0] = 1
    Z[alpha[1], 1] = 1
    return Z

