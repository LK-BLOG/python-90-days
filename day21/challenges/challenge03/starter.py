import functools

def cache(func):
    memo = {}
    @functools.wraps(func)
    def wrapper(*args):
        pass  # TODO: check memo, compute if missing
    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    print(fibonacci(30))  # 832040