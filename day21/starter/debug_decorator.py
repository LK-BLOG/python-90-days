import functools

# Exercise: Implement @debug decorator
# Should print: "calling func_name(args) -> result"

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pass  # TODO
    return wrapper

@debug
def add(a, b):
    return a + b

# Test
if __name__ == "__main__":
    result = add(1, 2)
    print(f"Result: {result}")