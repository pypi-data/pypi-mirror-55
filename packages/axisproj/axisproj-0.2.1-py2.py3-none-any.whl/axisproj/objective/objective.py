
class Objective(object):
    def __init__(self, name, alpha=1e4, threshold=0.6*2):
        self.name = name
        self.alpha = alpha
        self.threshold = threshold
        self._X = None
        self._n = 0
        self.XLXT = None
        self.XBXT = None

    @property
    def n(self):
        return self._n




