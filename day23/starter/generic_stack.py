from typing import TypeVar, Generic, list as ListType

T = TypeVar("T")

# Exercise: Implement a generic Stack class

class Stack(Generic[T]):
    def __init__(self):
        pass  # TODO

    def push(self, item: T) -> None:
        pass  # TODO

    def pop(self) -> T:
        pass  # TODO

    def peek(self) -> T:
        pass  # TODO

    def is_empty(self) -> bool:
        pass  # TODO

    def size(self) -> int:
        pass  # TODO

# Test
if __name__ == "__main__":
    s: Stack[int] = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.pop())   # 3
    print(s.peek())  # 2
    print(s.size())  # 2