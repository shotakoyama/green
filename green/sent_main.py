import numpy as np
from .load import load_dhrn_data, load_hdrn_data
from .score import (
        rn_accum_to_f,
        argmax,
        beta_to_alpha_beta)
from .verbose import NVerbose
from .result import f_result, table_result


def sent_main(args):
    if args.verbose:
        sent_verbose(args)
    else:
        sent_simple(args)


def sent_simple(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    _, _, _, dhrn_accum = load_dhrn_data(args)

    for hrn_accum in dhrn_accum:
        bh_score = [[
            rn_accum_to_f(rn_accum, alpha)
            for rn_accum in hrn_accum]
            for alpha, _ in params]
        bfs = [[
            f_result(score, args.digit)
            for score in h_score]
            for h_score in bh_score]
        fs = [f for fs in bfs for f in fs]
        line = '\t'.join(fs)
        print(line)


def sent_verbose(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    s_dat, rs_dat, hs_dat, dhrn_accum = load_dhrn_data(args)

    for d, hrn_accum in enumerate(dhrn_accum):
        for h, rn_accum in enumerate(hrn_accum):
            for alpha, beta in params:
                rnvb = [
                    NVerbose(n_accum, alpha, beta)
                    for n_accum
                    in rn_accum]
                rmax = argmax(rnvb)
                for r, nvb in enumerate(rnvb):
                    table = table_result(nvb, args.digit)
                    chosen = '*' if r == rmax else ' '
                    print(f'S-{d+1}   \t{s_dat[d]}')
                    print(f'H-{d+1}-{h+1} \t{hs_dat[d][h]}')
                    print(f'R-{d+1}-{r+1}{chosen}\t{rs_dat[d][r]}')
                    print(table)


def mean_main(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    _, _, _, hdrn_accum = load_hdrn_data(args)

    for drn_accum in hdrn_accum:
        bd_score = [[
            rn_accum_to_f(rn_accum, alpha)
            for rn_accum in drn_accum]
            for alpha, _ in params]
        fs = [np.mean(d_score) for d_score in bd_score]
        fs = [f_result(f, args.digit) for f in fs]
        line = '\t'.join(fs)
        print(line)

