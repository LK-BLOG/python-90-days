# Exercise: Implement Countdown iterator
# list(Countdown(5)) should return [5, 4, 3, 2, 1]

class Countdown:
    def __init__(self, start):
        pass  # TODO

    def __iter__(self):
        pass  # TODO

    def __next__(self):
        pass  # TODO

# Test
if __name__ == "__main__":
    result = list(Countdown(5))
    print(result)  # [5, 4, 3, 2, 1]