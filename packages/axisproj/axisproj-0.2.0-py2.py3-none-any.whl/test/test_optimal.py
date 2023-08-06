import sys
import pandas as pd
import numpy as np

from axisproj import optimal, objective


def main(arguments):
    data = pd.read_csv('../data/seawater.csv')
    data = data.values
    method = 'lpp'
    knn = 12

    if method == 'lpp':
        X = data.T
        obj = objective.LPPObjective(knn=knn,sigma=0.3)
    elif method == 'lde':
        X = data[:, :-1].T
        labs = np.ravel(data[:,-1])
        obj = objective.LDEObjective(knn=knn, labs=labs)
    else:
        print(f'Unknown method: {method}')
        return

    lp, ap = optimal(X, obj)
    print('LP:\n', lp)
    print('\nAP:\n', ap)


if __name__ == '__main__':
    main(sys.argv[1:])
