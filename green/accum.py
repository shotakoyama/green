from dataclasses import dataclass
from functools import cache


@dataclass
class Accumulator:
    true_keep: int = 0
    true_delete: int = 0
    true_insert: int = 0
    over_delete: int = 0
    over_insert: int = 0
    under_delete: int = 0
    under_insert: int = 0

    def __add__(self, other):
        tk = self.true_keep + other.true_keep
        td = self.true_delete + other.true_delete
        ti = self.true_insert + other.true_insert
        od = self.over_delete + other.over_delete
        oi = self.over_insert + other.over_insert
        ud = self.under_delete + other.under_delete
        ui = self.under_insert + other.under_insert
        return type(self)(tk, td, ti, od, oi, ud, ui)

    def true_positive(self):
        return self.true_keep + self.true_delete + self.true_insert

    def false_positive(self):
        return self.over_delete + self.over_insert

    def false_negative(self):
        return self.under_delete + self.under_insert

    @classmethod
    @cache # cache works very well
    def from_count(cls, s, r, h):
        stat = cls(
                min(s, r, h), # true keep
                max(0, s - max(r, h)), # true delete
                max(0, min(r, h) - s), # true inesrt
                max(0, min(s, r) - h), # over delete
                max(0, h - max(s, r)), # over insert
                max(0, min(s, h) - r), # under delete
                max(0, r - max(s, h))) # under insert
        return stat

