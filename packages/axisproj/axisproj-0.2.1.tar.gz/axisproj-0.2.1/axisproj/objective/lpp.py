import numpy as np
from sklearn.neighbors import kneighbors_graph

from .objective import Objective


class LPPObjective(Objective):
    def __init__(self, knn, sigma, **kwargs):
        super().__init__('lpp', **kwargs)
        self.knn = knn
        self.sigma = sigma

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, X):
        d, n = X.shape
        G = kneighbors_graph(X.T, self.knn, mode='distance', include_self=False).toarray()
        W = 0.5 * (G + G.T)
        W[W != 0] = np.exp(-W[W != 0] / (2 * self.sigma * self.sigma))
        D = np.diag(np.sum(W, axis=0))
        L = D - W

        self.XLXT = X.dot(L).dot(X.T)
        self.XBXT = X.dot(D).dot(X.T)  # since B = D for lpp