"""示例4：pytest 完整示例"""
import pytest


# 被测试的函数
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def is_palindrome(s):
    """检查是否是回文"""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def process_data(data):
    """处理数据"""
    if not data:
        return []
    return [x * 2 for x in data if isinstance(x, (int, float))]


# 基础测试
def test_add():
    assert add(2, 3) == 5

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)


# 参数化测试
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrize(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("input_val,expected", [
    ("racecar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
])
def test_is_palindrome(input_val, expected):
    assert is_palindrome(input_val) == expected


# Fixture
@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def empty_list():
    return []

def test_process_data_with_data(sample_list):
    result = process_data(sample_list)
    assert result == [2, 4, 6, 8, 10]

def test_process_data_empty(empty_list):
    result = process_data(empty_list)
    assert result == []


# 标记
@pytest.mark.slow
def test_large_data():
    """慢速测试"""
    large_list = list(range(1000000))
    result = process_data(large_list)
    assert len(result) == 1000000


# 异常测试
def test_process_data_invalid():
    """测试异常输入"""
    with pytest.raises(TypeError):
        process_data("not a list")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
