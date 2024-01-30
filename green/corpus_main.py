from .load import load_cdrn_data
from .score import (
        rn_accum_to_index,
        n_accum_to_gmeanf,
        beta_to_alpha_beta)
from .verbose import NVerbose
from .result import (
        round_half_up,
        f_result,
        table_result)
from .accum import Accumulator


def corpus_main(args):
    params = [beta_to_alpha_beta(beta) for beta in args.beta]
    _, _, _, cdrn_accum = load_cdrn_data(args)

    if args.verbose:
        corpus_verbose(args, params, cdrn_accum)
    else:
        corpus_simple_params(args, params)
        corpus_simple(args, params, cdrn_accum)


def corpus_simple_params(args, params):
    alpha_list = [round_half_up(alpha, args.digit) for alpha, _ in params]
    beta_list = [round_half_up(beta, args.digit) for _, beta in params]
    alpha_line = '\t'.join(['alpha'] + alpha_list)
    beta_line = '\t'.join(['beta'] + beta_list)
    print(alpha_line)
    print(beta_line)


def corpus_simple(args, params, cdrn_accum):
    for c, drn_accum in enumerate(cdrn_accum):
        bdn_accum = make_bdn_accum(drn_accum, params)
        bn_accum = make_bn_accum(bdn_accum, args.n)
        fs = [
            n_accum_to_gmeanf(n_accum, alpha)[-1]
            for n_accum, (alpha, _)
            in zip(bn_accum, params)]
        fs = [f_result(f, args.digit) for f in fs]
        line = '\t'.join([args.cor_path_list[c]] + fs)
        print(line)


def corpus_verbose(args, params, cdrn_accum):
    for c, drn_accum in enumerate(cdrn_accum):
        bdn_accum = make_bdn_accum(drn_accum, params)
        bn_accum = make_bn_accum(bdn_accum, args.n)
        for (alpha, beta), n_accum in zip(params, bn_accum):
            nvb = NVerbose(n_accum, alpha, beta)
            round_alpha = round_half_up(alpha, args.digit)
            round_beta = round_half_up(beta, args.digit)
            if args.line_verbose:
                line = nvb.line_verbose(args.digit)
                print(f'{round_alpha}\t{round_beta}\t{line}')
            else:
                table = table_result(nvb, args.digit)
                print(f'{args.cor_path_list[c]}\talpha={round_alpha}\tbeta={round_beta}')
                print(table)


# accumulate for all instances
def make_bn_accum(bdn_accum, max_n):
    bn_accum = [[
        sum([n_accum[n] for n_accum in dn_accum], start = Accumulator())
        for n in range(max_n)]
        for dn_accum in bdn_accum]
    return bn_accum


# choose the best references for each beta
def make_bdn_accum(drn_accum, params):
    bdn_accum = [
        make_dn_accum(drn_accum, alpha)
        for alpha, _ in params]
    return bdn_accum


# choose the best reference index for all instances
def make_dn_accum(drn_accum, alpha):
    dn_accum = [
        rn_accum[rn_accum_to_index(rn_accum, alpha)]
        for rn_accum in drn_accum]
    return dn_accum

