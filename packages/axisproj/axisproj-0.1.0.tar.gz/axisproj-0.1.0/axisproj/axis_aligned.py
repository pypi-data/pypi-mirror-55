import numpy as np
from numpy.linalg import norm, svd, eig
import cvxpy as cp

from .utils import compute_CB, make_basis


def find_axis_aligned(X, projections, max_size, knn):
    omega = []
    ap = dict()
    d = X.shape[0]

    for i, V in enumerate(projections):
        alphas = optimal_projection(X, V, omega,  max_size, knn)
        omega.extend(alphas)
        for alpha in alphas:
            if alpha not in ap:
                ap[alpha] = dict(alpha=alpha, LP=[])
            ap[alpha]['LP'].append(i)
    return list(ap.values())


def optimal_projection(X, V, global_omega, max_size, knn, delta=0.8):
    omega = []
    beta = []
    Z = []
    d = X.shape[0]

    Y = V.T.dot(X)
    while len(omega) < max_size:
        C, B = compute_CB(X, Y, knn)

        # step a
        indices = range(d)
        alpha = []
        for i in range(2):
            B1 = B
            if i > 0:
                B1 = B1 - C[:, alpha]
            B1 = np.tile(B1, (1, len(indices)))

            index = np.argmin(norm(C[:, indices] - B1, axis=0))
            alpha.append(indices[index])
            indices = np.delete(indices, index)

        if alpha[1] < alpha[0]:
            alpha = (alpha[1], alpha[0])
        else:
            alpha = (alpha[0], alpha[1])

        # distortion
        e = np.linalg.norm(C[:,alpha[0]] + C[:,alpha[1]] - B)

        # stop if it is not better than any of the AL projections for U
        if any(e > delta * norm(C[:,z[0]] + C[:,z[1]] - B) for z in omega):
            break

        # before accepting alpha, check if any previous alpha (in global omega) is good enough
        e /= delta
        for a in global_omega:
            ze = np.linalg.norm(C[:, a[0]] + C[:, a[1]] - B)
            if ze < e:
                alpha = a
                e = ze

        # step e
        Z.append(make_basis(d, alpha))
        beta = project(V, Z)
        if beta is None:
            Z.pop()
            break

        # step d
        omega.append(alpha)

        R = V.dot(V.T)
        for beta_i, Zi in zip(beta, Z):
            R -= beta_i * Zi.dot(Zi.T)

        # step f
        u, *_ = svd(R)
        U = u[:, 0:2]
        Y = U.T.dot(X)

    return omega


def project(V, Zlist, lvalue=1e-2):
    n = len(Zlist)
    ZZ = np.zeros((n, n))
    yZ = np.zeros((1, n))

    for i, Z in enumerate(Zlist):
        yZ[0, i] = norm(V.T.dot(Z), 'fro')
        for j in range(n):
            ZZ[i,j] = norm(Z.T.dot(Z), 'fro')

    u, *_ = eig(ZZ)
    min_u = np.min(u)
    if min_u < 0:
        ZZ = ZZ - min_u * np.eye(n)

    beta = cp.Variable(n)
    reg = cp.norm(beta,2)
    loss = cp.quad_form(beta, ZZ) - 2 * yZ * beta
    lambd = cp.Parameter(nonneg=True)
    problem = cp.Problem(cp.Minimize(loss + lambd * reg))
    lambd.value = lvalue
    problem.solve()

    return np.array(beta.value) if problem.status != 'unbounded' else None


