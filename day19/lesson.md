# Day 19: Iterator

## 1. Iterable vs Iterator

Any object implementing `__iter__()` is iterable (list, str, dict, set, file).
An iterator implements `__iter__()` + `__next__()`.

```python
nums = [1, 2, 3]
it = iter(nums)
print(next(it))  # 1
print(next(it))  # 2
# next(it) raises StopIteration
```

| | Iterable | Iterator |
|---|---|---|
| Methods | __iter__() | __iter__() + __next__() |
| State | No position memory | Tracks current position |
| Reuse | Yes (call iter again) | No (exhausted after use) |

### for loop truth
```python
for x in [1,2,3]: print(x)
# Equivalent to:
it = iter([1,2,3])
while True:
    try: x = next(it)
    except StopIteration: break
    print(x)
```

## 2. Custom Iterator

### Basic
```python
class CountUp:
    def __init__(self, start, end):
        self.current, self.end = start, end
    def __iter__(self):
        return self
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        v = self.current
        self.current += 1
        return v

for n in CountUp(1, 5):
    print(n)  # 1 2 3 4
```

### Fibonacci
```python
class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        v = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return v
```

### Infinite Iterator
```python
class CountFrom:
    def __init__(self, start=0, step=1):
        self.current, self.step = start, step
    def __iter__(self):
        return self
    def __next__(self):
        v = self.current
        self.current += self.step
        return v  # Never raises StopIteration - must break manually
```

### Common Mistakes
```python
# 1. __iter__ returns wrong type
class Bad:
    def __iter__(self):
        return [1, 2, 3]  # TypeError!

# 2. Forgetting StopIteration = infinite loop
class AlsoBad:
    def __init__(self):
        self.n = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.n += 1
        return self.n  # Never stops!
```

## 3. itertools Basics

```python
from itertools import chain, combinations, permutations, groupby, islice

# chain - link iterables
list(chain([1,2], [3,4], [5,6]))  # [1,2,3,4,5,6]

# combinations (order doesn't matter)
list(combinations("ABC", 2))  # [("A","B"),("A","C"),("B","C")]

# permutations (order matters)
list(permutations("AB", 2))  # [("A","B"),("B","A")]

# groupby (MUST sort first!)
data = [("A",1),("A",2),("B",3),("B",4)]
for k, g in groupby(data, key=lambda x: x[0]):
    print(k, list(g))

# islice - lazy slicing
list(islice(range(1000000), 5))  # [0,1,2,3,4]
list(islice(range(20), 2, 15, 3))  # [2,5,8,11,14]
```

## 4. Memory Advantage
```python
import sys
list_comp = [x**2 for x in range(1000000)]
gen_exp = (x**2 for x in range(1000000))
sys.getsizeof(list_comp)  # ~8MB
sys.getsizeof(gen_exp)    # ~200 bytes
```

## 5. File Line Reader
```python
class LineReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self._file = None
    def __iter__(self):
        return self
    def __next__(self):
        if self._file is None:
            self._file = open(self.filepath, "r", encoding="utf-8")
        line = self._file.readline()
        if not line:
            self._file.close()
            raise StopIteration
        return line.rstrip()
```

## Exercises
1. Countdown: list(Countdown(5)) == [5,4,3,2,1]
2. UniqueIterator: skip seen elements
3. itertools: chain + islice combo