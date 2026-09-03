# yield with send()
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)
print(acc.send(10))  # 10
print(acc.send(20))  # 30