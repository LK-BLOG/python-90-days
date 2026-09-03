import functools

# Exercise: Implement @singleton decorator
# Should ensure only one instance of the class is created

def singleton(cls):
    pass  # TODO

# Test
if __name__ == "__main__":
    @singleton
    class Config:
        def __init__(self):
            self.value = 42

    a = Config()
    b = Config()
    print(a is b)  # True