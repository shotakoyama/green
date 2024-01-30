from dataclasses import dataclass
from .accum import Accumulator


@dataclass
class NgramStat:
    src_dict: dict
    ref_dict: dict
    cor_dict: dict

    def __getitem__(self, key):
        s = self.src_dict.get(key, 0)
        r = self.ref_dict.get(key, 0)
        c = self.cor_dict.get(key, 0)
        return s, r, c

    def keys(self):
        return set.union(
            set(self.src_dict),
            set(self.ref_dict),
            set(self.cor_dict))

    def accumulate(self):
        lst = [
            Accumulator.from_count(*self[key])
            for key
            in self.keys()]
        return sum(lst, start = Accumulator())

