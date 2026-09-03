import functools, time

def retry(max_attempts=3, delay=0.1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass  # TODO: retry logic
        return wrapper
    return decorator

call_count = 0

@retry(max_attempts=3, delay=0.01)
def flaky():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("fail")
    return "success"

if __name__ == "__main__":
    print(flaky())