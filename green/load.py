from .aggreg import (
        make_dhrn_accum,
        make_hdrn_accum)


def load_corpora(args):
    s_dat = load_text(args.source_path)
    rs_dat = load_paired_texts(args.ref_path_list)
    hs_dat = load_paired_texts(args.hyp_path_list)
    assert len(s_dat) == len(rs_dat) == len(hs_dat)
    return s_dat, rs_dat, hs_dat


def load_corpora_T(args):
    s_dat = load_text(args.source_path)
    rs_dat = load_paired_texts(args.ref_path_list)
    h_dats = [load_text(path) for path in args.hyp_path_list]
    assert len(s_dat) == len(rs_dat)
    assert all(len(s_dat) == len(hyp) for hyp in h_dats)
    return s_dat, rs_dat, h_dats


def load_text(path):
    with open(path) as f:
        data = [x.rstrip('\n') for x in f]
    return data


def load_paired_texts(path_list):
    data = [load_text(path) for path in path_list]
    return list(zip(*data))


def load_dhrn_data(args):
    s_dat, rs_dat, hs_dat = load_corpora(args)
    dhrn_accum = make_dhrn_accum(args.n, s_dat, rs_dat, hs_dat)
    return s_dat, rs_dat, hs_dat, dhrn_accum


def load_hdrn_data(args):
    s_dat, rs_dat, h_dats = load_corpora_T(args)
    hdrn_accum = make_hdrn_accum(args.n, s_dat, rs_dat, h_dats)
    return s_dat, rs_dat, h_dats, hdrn_accum

