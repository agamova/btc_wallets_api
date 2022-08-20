import string

from decimal import Decimal, ROUND_HALF_DOWN
from random import choices


def get_decimal_rate(rate):
    return Decimal(rate).quantize(
        Decimal('.0000000001'),
        rounding=ROUND_HALF_DOWN
    )


def get_address():
    return ''.join(choices(['1', '3'])) + ''.join(choices(string.ascii_letters + string.digits, k=33))
