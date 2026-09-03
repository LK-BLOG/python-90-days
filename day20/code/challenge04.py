# Challenge 04: Coroutine Accumulator

def accumulator():
    pass  # TODO: implement coroutine with yield/send

# Test
if __name__ == "__main__":
    acc = accumulator()
    next(acc)  # prime
    print(acc.send(10))   # 10
    print(acc.send(20))   # 30
    print(acc.send(5))    # 35