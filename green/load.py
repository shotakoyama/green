from .aggreg import (
        make_dcrn_accum,
        make_cdrn_accum)


def load_corpora(args):
    s_dat = load_text(args.source_path)
    rs_dat = load_paired_texts(args.ref_path_list)
    cs_dat = load_paired_texts(args.cor_path_list)
    assert len(s_dat) == len(rs_dat) == len(cs_dat)
    return s_dat, rs_dat, cs_dat


def load_corpora_T(args):
    s_dat = load_text(args.source_path)
    rs_dat = load_paired_texts(args.ref_path_list)
    c_dats = [load_text(path) for path in args.cor_path_list]
    assert len(s_dat) == len(rs_dat)
    assert all(len(s_dat) == len(cor) for cor in c_dats)
    return s_dat, rs_dat, c_dats


def load_text(path):
    with open(path) as f:
        data = [x.rstrip('\n') for x in f]
    return data


def load_paired_texts(path_list):
    data = [load_text(path) for path in path_list]
    return list(zip(*data))


def load_dcrn_data(args):
    s_dat, rs_dat, cs_dat = load_corpora(args)
    dcrn_accum = make_dcrn_accum(args.n, s_dat, rs_dat, cs_dat)
    return s_dat, rs_dat, cs_dat, dcrn_accum


def load_cdrn_data(args):
    s_dat, rs_dat, c_dats = load_corpora_T(args)
    cdrn_accum = make_cdrn_accum(args.n, s_dat, rs_dat, c_dats)
    return s_dat, rs_dat, c_dats, cdrn_accum

