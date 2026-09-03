"""pytest 核心功能演示"""

import pytest


def word_count(text: str) -> int:
    """计算单词数"""
    return len(text.strip().split())


def add(a: int, b: int) -> int:
    return a + b


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


# === pytest fixture 示例 ===
@pytest.fixture
def empty_stack():
    return Stack()


@pytest.fixture
def filled_stack():
    s = Stack()
    for i in range(5):
        s.push(i)
    return s


# === parametrize 示例 ===
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -100, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("input_val,expected", [
    ("hello", 1),
    ("hello world", 2),
    ("  spaces  ", 1),
    ("", 0),
])
def test_word_count(input_val, expected):
    assert word_count(input_val) == expected


# === fixture 测试 ===
def test_stack_push_pop(empty_stack):
    empty_stack.push(42)
    assert empty_stack.pop() == 42
    assert empty_stack.is_empty()


def test_stack_peek(filled_stack):
    assert filled_stack.peek() == 4
    assert filled_stack.size() == 5


def test_stack_pop_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()


@pytest.mark.slow
def test_stack_large():
    s = Stack()
    for i in range(10000):
        s.push(i)
    for i in range(9999, -1, -1):
        assert s.pop() == i


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
