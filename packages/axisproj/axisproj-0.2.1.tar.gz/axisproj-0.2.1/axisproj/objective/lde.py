import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

from .objective import Objective


class LDEObjective(Objective):
    def __init__(self, knn, labs, alpha=5e2, threshold=0.5*2):
        super().__init__('lde', alpha, threshold)
        self.knn = knn
        self.labs = labs

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, X):
        self._X = X
        d, n = X.shape
        Gw = np.zeros((n, n))
        Gb = np.zeros((n, n))

        dists = pairwise_distances(X.T)

        for i in range(n):
            inds = np.where(self.labs == self.labs[i])[0]
            sinds = np.argsort(dists[i, inds])
            Gw[i, inds[sinds[:self.knn]]] = 1

            inds = np.where(self.labs != self.labs[i])[0]
            sinds = np.argsort(dists[i, inds])
            Gb[i, inds[sinds[:self.knn]]] = 1

        Gw = np.maximum(Gw, Gw.T)
        Bw = np.diag(np.sum(Gw, axis=0))
        Lw = Bw - Gw
        self.XLXT = X.dot(Lw).dot(X.T)

        Gb = np.maximum(Gb, Gb.T)
        Bb = np.diag(np.sum(Gb, axis=0))
        Lb = Bb - Gb
        self.XBXT = X.dot(Lb).dot(X.T)