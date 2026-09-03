# Exercise: Implement generator-based filter and map

def gen_filter(func, iterable):
    pass  # TODO

def gen_map(func, iterable):
    pass  # TODO

# Test
if __name__ == "__main__":
    nums = range(10)
    evens = list(gen_filter(lambda x: x % 2 == 0, nums))
    print(evens)  # [0, 2, 4, 6, 8]
    doubled = list(gen_map(lambda x: x * 2, evens))
    print(doubled)  # [0, 4, 8, 12, 16]