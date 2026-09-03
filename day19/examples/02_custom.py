# Custom iterator
class Range2:
    def __init__(self, stop):
        self.current, self.stop = 0, stop
    def __iter__(self):
        return self
    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

for n in Range2(5):
    print(n, end=" ")