"""可调用对象"""
class Accumulator:
    def __init__(self, initial=0):
        self.total = initial
    def __call__(self, value):
        self.total += value
        return self.total

acc = Accumulator()
print(acc(10))   # 10
print(acc(20))   # 30
print(acc(5))    # 35
print(callable(acc))  # True

class cached:
    def __init__(self, func):
        self.func = func
        self._cache = {}
    def __call__(self, *args):
        if args not in self._cache:
            self._cache[args] = self.func(*args)
        return self._cache[args]

@cached
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
print(fib(100))  # 354224848179261915075
