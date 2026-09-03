from typing import TypeVar, Sequence

T = TypeVar("T")

def first(lst: Sequence[T]) -> T:
    return lst[0]

def second(lst: Sequence[T]) -> T:
    return lst[1]

print(first([1, 2, 3]))    # 1
print(first(["a", "b"]))   # "a"
print(second([1, 2, 3]))   # 2