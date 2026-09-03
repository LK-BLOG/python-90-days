# -*- coding: utf-8 -*-
squares = [x**2 for x in range(1, 6)]
print(squares)

evens = [x for x in range(20) if x % 2 == 0]
print(evens)

sq_dict = {x: x**2 for x in range(1, 6)}
print(sq_dict)
