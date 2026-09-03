# Day 21: Decorators

## 1. Closures Review -> Decorators
A decorator is just a function that takes a function and returns a new function.

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before call
# Hello!
# After call
```

## 2. functools.wraps
Always use `@functools.wraps(func)` to preserve metadata.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

## 3. Decorators with Arguments
```python
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello {name}")

greet("World")  # prints 3 times
```

## 4. Class Decorators
```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def add(a, b):
    return a + b

print(add(1, 2))  # 3
print(add.count)   # 1
```

## 5. Decorator Stacking Order
```python
@decorator_a
@decorator_b
def func():
    pass
# Equivalent to: func = decorator_a(decorator_b(func))
# decorator_b wraps first, then decorator_a wraps that
```

## 6. Built-in Decorators

### property
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

### staticmethod / classmethod
```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def from_string(cls, s):
        a, b = map(int, s.split("+"))
        return cls()
```

## 7. Practical Decorators

### @timer
```python
import time, functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

### @retry
```python
import functools, time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
```

### @cache (simple memoization)
```python
def cache(func):
    memo = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### @validate
```python
def validate(**rules):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # validation logic here
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Exercises
1. Implement @debug decorator (print function name and args)
2. Implement @singleton decorator (only one instance)
3. Implement @timeout decorator (cancel if too slow)