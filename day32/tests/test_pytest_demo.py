"""测试 pytest_demo 模块"""
import sys
sys.path.insert(0, "../examples")
from pytest_demo import word_count, add, Stack

def test_add_basic():
    assert add(1, 2) == 3

def test_word_count_basic():
    assert word_count("hello world") == 2

def test_stack_basic():
    s = Stack()
    s.push(1)
    assert s.pop() == 1
