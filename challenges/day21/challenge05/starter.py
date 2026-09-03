import functools, time

def smart_decorator(func=None, *, rate_limit=None, cache_ttl=None, retry_count=1):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            pass  # TODO: apply rate_limit, cache, retry
        return wrapper
    if func is not None:
        return decorator(func)
    return decorator

@smart_decorator(rate_limit=2, cache_ttl=60)
def get_data(key):
    return f"data_{key}"

if __name__ == "__main__":
    print(get_data("test"))