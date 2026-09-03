from typing import TypeVar, Generic

T = TypeVar("T")

class Container(Generic[T]):
    def __init__(self, items=None):
        pass  # TODO

    def add(self, item: T) -> None:
        pass  # TODO

    def get_all(self) -> list[T]:
        pass  # TODO

# Test
if __name__ == "__main__":
    c: Container[int] = Container()
    c.add(1)
    c.add(2)
    print(c.get_all())  # [1, 2]