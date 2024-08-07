import numpy as np
from .load import load_dcrn_data, load_cdrn_data
from .score import (
        rn_accum_to_f,
        argmax,
        beta_to_alpha_beta)
from .verbose import NVerbose
from .result import (
        f_result,
        table_result,
        print_param_header)


def sent_main(args):
    if args.verbose:
        sent_verbose(args)
    else:
        sent_simple(args)


def sent_simple(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    _, _, _, dcrn_accum = load_dcrn_data(args)

    for crn_accum in dcrn_accum:
        bc_score = [[
            rn_accum_to_f(rn_accum, alpha)
            for rn_accum in crn_accum]
            for alpha, _ in params]
        bfs = [[
            f_result(score, args.digit)
            for score in c_score]
            for c_score in bc_score]
        fs = [f for fs in bfs for f in fs]
        line = '\t'.join(fs)
        print(line)


def sent_verbose(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    s_dat, rs_dat, cs_dat, dcrn_accum = load_dcrn_data(args)

    for d, crn_accum in enumerate(dcrn_accum):
        for c, rn_accum in enumerate(crn_accum):
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
                    print(f'C-{d+1}-{c+1} \t{cs_dat[d][c]}')
                    print(f'R-{d+1}-{r+1}{chosen}\t{rs_dat[d][r]}')
                    print(table)


def mean_main(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    _, _, _, cdrn_accum = load_cdrn_data(args)
    print_param_header(params, args.digit)

    for c, drn_accum in enumerate(cdrn_accum):
        bd_score = [[
            rn_accum_to_f(rn_accum, alpha)
            for rn_accum in drn_accum]
            for alpha, _ in params]
        fs = [np.mean(d_score) for d_score in bd_score]
        fs = [f_result(f, args.digit) for f in fs]
        line = '\t'.join([args.cor_path_list[c]] + fs)
        print(line)

