# Fibonacci iterator
class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        v = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return v

for num in Fibonacci(10):
    print(num, end=" ")