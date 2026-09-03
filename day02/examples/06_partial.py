# -*- coding: utf-8 -*-
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(5))  # 25

binary_to_int = partial(int, base=2)
print(binary_to_int("1010"))  # 10
