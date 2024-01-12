import numpy as np
from .score import (
        precision,
        recall,
        f_score)
from .result import round_half_up


class NVerbose:

    def __init__(self, n_accum, alpha, beta):
        self.header = [
            '', 'tk', 'td', 'ti',
            'od', 'oi', 'ud', 'ui',
            'TP', 'FP', 'FN',
            'P', 'R', f'F{beta}',
            'cumP', 'cumR', 'cumF']
        self.n = len(n_accum)

        self.tks = [accum.true_keep for accum in n_accum]
        self.tds = [accum.true_delete for accum in n_accum]
        self.tis = [accum.true_insert for accum in n_accum]
        self.ods = [accum.over_delete for accum in n_accum]
        self.ois = [accum.over_insert for accum in n_accum]
        self.uds = [accum.under_delete for accum in n_accum]
        self.uis = [accum.under_insert for accum in n_accum]

        self.tps = [tk + td + ti for tk, td, ti in zip(self.tks, self.tds, self.tis)]
        self.fps = [od + oi for od, oi in zip(self.ods, self.ois)]
        self.fns = [ud + ui for ud, ui in zip(self.uds, self.uis)]

        self.ps = [precision(tp, fp) for tp, fp in zip(self.tps, self.fps)]
        self.rs = [recall(tp, fn) for tp, fn in zip(self.tps, self.fns)]
        self.fs = [f_score(p, r, alpha) for p, r in zip(self.ps, self.rs)]

        with np.errstate(divide = 'ignore'):
            logps = np.log(self.ps)
            logrs = np.log(self.rs)

        self.mcps = np.exp(logps.cumsum(axis = 0) / np.arange(1, logps.shape[0] + 1))
        self.mcrs = np.exp(logrs.cumsum(axis = 0) / np.arange(1, logrs.shape[0] + 1))
        self.mcfs = [f_score(p, r, alpha) for p, r in zip(self.mcps, self.mcrs)]

    def iter_row(self, digit):
        for n in range(self.n):
            lst = [
                n + 1, self.tks[n], self.tds[n], self.tis[n],
                self.ods[n], self.ois[n], self.uds[n], self.uis[n],
                self.tps[n], self.fps[n], self.fns[n],
                round_half_up(100 * self.ps[n], digit),
                round_half_up(100 * self.rs[n], digit),
                round_half_up(100 * self.fs[n], digit),
                round_half_up(100 * self.mcps[n], digit),
                round_half_up(100 * self.mcrs[n], digit),
                round_half_up(100 * self.mcfs[n], digit)]
            yield lst

    def line_verbose(self, digit):
        p = round_half_up(100 * self.mcps[self.n - 1], digit)
        r = round_half_up(100 * self.mcrs[self.n - 1], digit)
        f = round_half_up(100 * self.mcfs[self.n - 1], digit)
        return f'{p}\t{r}\t{f}'

    def __lt__(self, other):
        return self.mcfs[::-1] < other.mcfs[::-1]

