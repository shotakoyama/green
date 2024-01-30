import numpy as np
from functools import cache


def rn_accum_to_f(rn_accum, alpha):
    rfs = rn_accum_to_r_reversed_fs(rn_accum, alpha)
    return max(rfs)[0] # f of 1~N


def rn_accum_to_index(rn_accum, alpha):
    rfs = rn_accum_to_r_reversed_fs(rn_accum, alpha)
    return argmax(rfs)


def rn_accum_to_r_reversed_fs(rn_accum, alpha):
    r_fs = [
        n_accum_to_gmeanf(n_accum, alpha)[::-1]
        for n_accum
        in rn_accum]
    return r_fs


def n_accum_to_gmeanf(n_accum, alpha):
    prs = [
        accum_to_pr(accum)
        for accum
        in n_accum]
    prs = np.array(prs, dtype = float)

    # geometric mean of p and r
    # [[p of 1, r of 1], [p of 1~2, r of 1~2], [p of 1~3, r of 1~3], ...]
    with np.errstate(divide = 'ignore'):
        logprs = np.log(prs)
    meancumprs = np.exp(
            logprs.cumsum(axis = 0)
            /
            np.arange(1, logprs.shape[0] + 1)[:, np.newaxis])

    # [f of 1, f of 1~2, ..., f of 1~N]
    fs = [
        f_score(p, r, alpha)
        for p, r
        in meancumprs]
    return fs


def accum_to_pr(accum):
    tp = accum.true_positive()
    fp = accum.false_positive()
    fn = accum.false_negative()
    p = precision(tp, fp)
    r = recall(tp, fn)
    return p, r


@cache
def precision(tp, fp):
    return tp / (tp + fp) if tp + fp > 0 else 1.0


@cache
def recall(tp, fn):
    return tp / (tp + fn) if tp + fn > 0 else 0.0


def f_score(p, r, alpha):
    if p == 0 or r == 0:
        f = 0
    else:
        f = 1 / (alpha / p + (1 - alpha) / r)
    return f


def argmax(xs):
    return max(enumerate(xs), key = lambda x: x[1])[0]


def make_params(betas):
    return [beta_to_alpha_beta(beta) for beta in betas]


# convert beta -> alpha
def beta_to_alpha_beta(beta):
    if beta == 'inf' or beta == 'Inf':
        alpha = 0
        beta = np.inf
    else:
        alpha = 1 / (beta ** 2 + 1)
    return alpha, beta

