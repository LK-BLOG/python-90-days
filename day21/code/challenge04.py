import functools

def validate(**rules):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass  # TODO: validate args against rules
        return wrapper
    return decorator

@validate(age=(int, 0, 150), name=(str, None, None))
def create_person(name, age):
    return {"name": name, "age": age}

if __name__ == "__main__":
    print(create_person("Alice", 30))
    try:
        print(create_person("Bob", -5))
    except ValueError as e:
        print(f"Validation error: {e}")