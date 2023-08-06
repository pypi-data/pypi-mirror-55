import numpy as np

from .objective import Objective


class PCAObjective(Objective):
    def __init__(self, **kwargs):
        super().__init__('pca', **kwargs)
        self.alpha = -self.alpha

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, X):
        d, n = X.shape
        W = np.zeros((n, n))
        v = 1.0/n
        for i in range(n-1):
            for j in range(i+1, n):
                W[i,j] = v
        W = W + W.T
        D = np.eye(n)
        L = D - W
        self.XLXT = X.dot(L).dot(X.T)
        self.XBXT = np.eye(d)
