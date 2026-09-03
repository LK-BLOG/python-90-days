# Day 20: Generators

## 1. yield Basics
Generators are functions that use `yield` instead of return.
They are iterators - every generator is an iterator.

```python
def countdown(n):
    while n > 0:
        yield n  # pauses here, returns value
        n -= 1

for num in countdown(5):
    print(num)  # 5 4 3 2 1
```

## 2. Generator is an Iterator
```python
def simple():
    yield 1
    yield 2
    yield 3

g = simple()
print(type(g))  # generator
print(next(g))  # 1
print(next(g))  # 2
print(next(g))  # 3
# next(g) raises StopIteration
```

## 3. yield as Expression (send)
yield can receive values via send()

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)          # prime the generator
acc.send(10)       # 10
acc.send(20)       # 30
acc.send(5)        # 35
```

## 4. yield from (Delegation)
```python
def inner():
    yield 1
    yield 2

def outer():
    yield from inner()
    yield 3

list(outer())  # [1, 2, 3]

# Flattening with yield from
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4], 5], 6]))  # [1,2,3,4,5,6]
```

## 5. Generator Expressions vs List Comprehensions
```python
# List comprehension - immediate, uses memory
nums = [x**2 for x in range(1000000)]

# Generator expression - lazy, constant memory
nums = (x**2 for x in range(1000000))

# Generator function
def gen_squares(n):
    for x in range(n):
        yield x**2
```

## 6. Generator Pipelines
```python
def read_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith("#"):
            yield line

def split_words(lines):
    for line in lines:
        yield from line.split()

# Pipeline: files -> lines -> non-comments -> words
words = split_words(filter_comments(read_lines("data.txt")))
```

## 7. Coroutine Basics
```python
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

avg =averager()
next(avg)
print(avg.send(10))   # 10.0
print(avg.send(20))   # 15.0
print(avg.send(30))   # 20.0
```

## 8. itertools Advanced
```python
from itertools import islice, takewhile, dropwhile, starmap, cycle

# takewhile - take while condition is true
list(takewhile(lambda x: x < 5, [1,3,5,2,1]))  # [1,3]

# dropwhile - skip while condition is true
list(dropwhile(lambda x: x < 5, [1,3,5,2,1]))  # [5,2,1]

# cycle - infinite cycling
c = cycle([1,2,3])
[next(c) for _ in range(7)]  # [1,2,3,1,2,3,1]
```

## Exercises
1. Implement generator-based range
2. Implement generator-based map/filter
3. Build a pipeline: read -> filter -> transform -> collect