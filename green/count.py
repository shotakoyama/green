from collections import Counter
from functools import cache


split_ngram = None


def set_tokenization(tokenization):
    global split_ngram
    assert split_ngram is None # resetting split_ngram is prohibited

    if tokenization == 'char':
        split_ngram = split_char_ngram
    elif tokenization == 'word':
        split_ngram = split_word_ngram
    else:
        assert False


@cache
def ngram_counter(n, sent):
    ngram_list = split_ngram(n, sent)
    return dict(Counter(ngram_list))


def split_char_ngram(n, sent):
    return [sent[i : i + n] for i in range(len(sent) - n + 1)]


def split_word_ngram(n, sent):
    sent = sent.split()
    return [' '.join(sent[i : i + n]) for i in range(len(sent) - n + 1)]

