# Day 16: 魔术方法

## 1. 字符串表示

### 1.1 __repr__ vs __str__

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        '''开发者看的：可以重建对象'''
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        '''用户看的：友好显示'''
        return f'({self.x}, {self.y})'

p = Point(3, 4)
print(repr(p))  # Point(3, 4) -- 开发调试用
print(str(p))   # (3, 4)    -- 用户看的
print(p)        # (3, 4)    -- 默认调用 __str__
```

### 1.2 __format__

```python
class Money:
    def __init__(self, amount, currency='CNY'):
        self.amount = amount
        self.currency = currency

    def __format__(self, fmt):
        if fmt == 'f':
            return f'{self.currency} {self.amount:,.2f}'
        elif fmt == 'r':
            return f'{self.currency}{self.amount}'
        return str(self)

price = Money(12345.678)
print(f'{price:f}')  # CNY 12,345.68
print(f'{price:r}')  # CNY12345.678
print(format(price)) # CNY 12,345.678
```

---

## 2. 比较运算符

### 2.1 富比较方法

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return self.score != other.score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

s1 = Student('Alice', 90)
s2 = Student('Bob', 85)
print(s1 > s2)   # True
print(s1 == s2)  # False
print(s1 >= s1)  # True
```

### 2.2 functools.total_ordering 简化

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score
    # 自动补全 __le__, __gt__, __ge__
```

---

## 3. __hash__

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(1, 2)
points = {p1, p2}
print(len(points))  # 1（相等的对象去重）
```

---

## 4. 容器协议

### 4.1 __len__ 和 __bool__

```python
class Collection:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return len(self._items) > 0

c = Collection([1, 2, 3])
print(len(c))     # 3
print(bool(c))    # True
print(bool(Collection([])))  # False
```

### 4.2 __getitem__/__setitem__/__delitem__

```python
class SparseArray:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data.get(key, 0)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

arr = SparseArray()
arr[100] = 42
print(arr[100])   # 42
print(arr[50])    # 0（默认值）
del arr[100]
```

### 4.3 __contains__ 和 __iter__

```python
class WordCollection:
    def __init__(self, words):
        self._words = list(words)

    def __contains__(self, word):
        return word in self._words

    def __iter__(self):
        return iter(self._words)

    def __getitem__(self, index):
        return self._words[index]

wc = WordCollection(['hello', 'world'])
print('hello' in wc)  # True
for w in wc:
    print(w)          # hello, world
print(wc[0])          # hello
```

---

## 5. __call__

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
print(callable(double))  # True
```

### 函数缓存装饰器示例

```python
class cached:
    def __init__(self, func):
        self.func = func
        self._cache = {}

    def __call__(self, *args):
        if args not in self._cache:
            self._cache[args] = self.func(*args)
        return self._cache[args]

@cached
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # 瞬间计算
```

---

## 6. 运算符重载

### 6.1 算术运算符

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):      # +
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):      # -
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):     # *
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar): # /
        return Vector(self.x / scalar, self.y / scalar)

    def __neg__(self):             # 取负
        return Vector(-self.x, -self.y)

    def __abs__(self):             # abs()
        return (self.x**2 + self.y**2)**0.5

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)    # Vector(4, 6)
print(v1 * 3)     # Vector(3, 6)
print(abs(v1))    # 2.236...
```

### 6.2 反向运算符

```python
class Vector:
    # ... 前面的定义 ...

    def __rmul__(self, scalar):  # 右乘：3 * v
        return self.__mul__(scalar)
```

### 6.3 就地运算符

```python
class Vector:
    # ...
    def __iadd__(self, other):  # +=
        self.x += other.x
        self.y += other.y
        return self
```

---

## 7. 上下文管理器

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.duration = time.time() - self.start
        print(f'耗时: {self.duration:.2f}秒')
        return False

with Timer() as t:
    sum(range(1000000))
# 耗时: 0.03秒
```

---

## 本日总结

| 概念 | 方法 | 用途 |
|------|------|------|
| 字符串 | __repr__, __str__, __format__ | 表示和格式化 |
| 比较 | __eq__, __lt__, etc. | 对象比较 |
| 容器 | __len__, __getitem__, __contains__ | 序列/集合行为 |
| 运算 | __add__, __mul__, etc. | 数学运算 |
| 可调用 | __call__ | 像函数一样使用 |
| 上下文 | __enter__, __exit__ | with 语句 |
