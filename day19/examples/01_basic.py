# Basic iterator usage
nums = [10, 20, 30]
it = iter(nums)
print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
try:
    next(it)
except StopIteration:
    print("Iterator exhausted")