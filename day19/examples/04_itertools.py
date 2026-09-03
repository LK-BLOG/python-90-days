# itertools basics
from itertools import chain, combinations, permutations, groupby, islice

print(list(chain([1,2], [3,4], [5,6])))
print(list(combinations("ABC", 2)))
print(list(permutations("AB", 2)))

data = [("A",1),("A",2),("B",3),("B",4)]
for k, g in groupby(data, key=lambda x: x[0]):
    print(k, list(g))

print(list(islice(range(100), 0, 20, 3)))