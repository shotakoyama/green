from decimal import Decimal, ROUND_HALF_UP
from prettytable import PrettyTable


def round_half_up(x, digit):
    digit = Decimal('0.' + '0' * digit)
    x = Decimal(str(x)).quantize(digit, rounding = ROUND_HALF_UP)
    return str(x)


def f_result(f, digit):
    f = 100 * f
    f = round_half_up(f, digit)
    return f


def table_result(nvb, digit):
    table = PrettyTable(nvb.header)
    for lst in nvb.iter_row(digit):
        table.add_row(lst)
    return table


def print_param_header(params, digit):
    alpha_list = [round_half_up(alpha, digit) for alpha, _ in params]
    beta_list = [round_half_up(beta, digit) for _, beta in params]
    alpha_line = '\t'.join(['alpha'] + alpha_list)
    beta_line = '\t'.join(['beta'] + beta_list)
    print(alpha_line)
    print(beta_line)

