# -*- coding: utf-8 -*-
def apply_twice(func, value):
    return func(func(value))

def add_five(x):
    return x + 5

print(apply_twice(add_five, 10))  # 20
