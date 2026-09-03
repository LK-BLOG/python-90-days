# -*- coding: utf-8 -*-
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)

evens = list(filter(lambda x: x % 2 == 0, range(1, 11)))
print(evens)
