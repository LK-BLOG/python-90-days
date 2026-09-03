# Exercise: Implement generator-based range

def gen_range(*args):
    pass  # TODO: yield numbers like range()

# Test
if __name__ == "__main__":
    print(list(gen_range(5)))      # [0,1,2,3,4]
    print(list(gen_range(1, 5)))   # [1,2,3,4]
    print(list(gen_range(0, 10, 2)))  # [0,2,4,6,8]