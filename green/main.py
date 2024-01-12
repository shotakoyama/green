from argparse import ArgumentParser
from .sent_main import sent_main, mean_main
from .corpus_main import corpus_main
from .count import set_tokenization


def green():
    main(corpus_main)


def sgreen():
    main(sent_main)


def mgreen():
    main(mean_main)


def main(handler):
    parser = ArgumentParser()
    add_args(parser)
    parser.set_defaults(handler = handler)
    args = parser.parse_args()
    set_tokenization(args.tokenization)
    args.handler(args)


def add_args(parser):
    parser.add_argument(
            '-n', type = int, default = 4,
            help = 'maximum n for n-gram')
    parser.add_argument(
            '-s', '--src', '--source',
            required = True,
            dest = 'source_path')
    parser.add_argument(
            '-r', '--ref', '--refs', '--references',
            required = True,
            nargs = '+',
            dest = 'ref_path_list')
    parser.add_argument(
            '-o', '--out', '--outs', '--outputs',
            '--hyp', '--hyps', '--hypotheses',
            required = True,
            nargs = '+',
            dest = 'hyp_path_list')
    parser.add_argument(
            '-b', '--beta', dest = 'beta',
            type = float, default = [1.0], nargs = '+',
            help = 'beta for F score calculation')
    parser.add_argument(
            '-d', '--digit', dest = 'digit',
            type = int, default = 2,
            help = 'digit of quantization')
    parser.add_argument(
            '-t', '--token', '--tokenize',
            '--tokenization', dest = 'tokenization',
            choices = ['char', 'word'],
            default = 'word')
    parser.add_argument(
            '-v', '--verbose', dest = 'verbose',
            action = 'store_true')
    parser.add_argument(
            '-l', '--line-verbose', dest = 'line_verbose',
            action = 'store_true')

