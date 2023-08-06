from sklearn.preprocessing import StandardScaler
from scipy.special import comb

from .linear import find_linear_projections
from .axis_aligned import find_axis_aligned
from .evidence import compute_evidence
from .precision_recall import histogram
from .utils import make_basis


def optimal(X, objective, normalize=True, knn=12, hist=histogram()):
    d, n = X.shape
    if normalize:
        X = StandardScaler().fit_transform(X.T).T

    projections = find_linear_projections(X, 2, objective)

    l = min(5, int(comb(d,2)/3))
    axis_projections = find_axis_aligned(X, projections, l, knn)

    evidence = compute_evidence(axis_projections, X, projections, knn)

    for ap in axis_projections:
        alpha = ap['alpha']
        ap['evidence'] = evidence[alpha]
        ap['histogram'] = hist(make_basis(d, alpha), X)

    sorted(axis_projections, key=lambda p: p['evidence'], reverse=True)

    linear_projections = [dict(V=V, histogram=hist(V, X), AP=[]) for V in projections]

    for i, ap in enumerate(axis_projections):
        for lp in ap['LP']:
            linear_projections[lp]['AP'].append(i)

    return linear_projections, axis_projections
