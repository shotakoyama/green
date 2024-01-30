from functools import cache
from .count import ngram_counter
from .ngram import NgramStat


def make_dcrn_accum(max_n, s_dat, rs_dat, cs_dat):
    return [
        make_crn_accum(max_n, s, rs, cs)
        for s, rs, cs
        in zip(s_dat, rs_dat, cs_dat)]


def make_crn_accum(max_n, s, rs, cs):
    return [
        make_rn_accum(max_n, s, rs, c)
        for c in cs]


def make_cdrn_accum(max_n, s_dat, rs_dat, c_dats):
    return [
        make_drn_accum(max_n, s_dat, rs_dat, c_dat)
        for c_dat in c_dats]


def make_drn_accum(max_n, s_dat, rs_dat, c_dat):
    return [
        make_rn_accum(max_n, s, rs, c)
        for s, rs, c
        in zip(s_dat, rs_dat, c_dat)]


def make_rn_accum(max_n, s, rs, c):
    return [
        make_n_accum(max_n, s, r, c)
        for r in rs]


@cache
def make_n_accum(max_n, s, r, c):
    return [
        make_accum(n, s, r, c)
        for n
        in range(1, max_n + 1)]


def make_accum(n, s, r, c):
    s_cnt = ngram_counter(n, s)
    r_cnt = ngram_counter(n, r)
    c_cnt = ngram_counter(n, c)
    accum = NgramStat(s_cnt, r_cnt, c_cnt).accumulate()
    return accum

