import functools, time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pass  # TODO: measure and print time
    return wrapper

@timer
def slow_function():
    time.sleep(0.1)
    return "done"

if __name__ == "__main__":
    result = slow_function()
    print(result)