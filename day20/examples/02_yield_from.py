# yield from delegation
def inner_gen():
    yield "a"
    yield "b"

def outer_gen():
    yield from inner_gen()
    yield "c"

print(list(outer_gen()))  # ["a", "b", "c"]