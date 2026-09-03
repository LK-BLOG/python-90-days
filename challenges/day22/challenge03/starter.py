from contextlib import contextmanager

@contextmanager
def suppress(*exception_types):
    pass  # TODO

# Test
if __name__ == "__main__":
    with suppress(ValueError, KeyError):
        raise ValueError("test")
    print("No error!")