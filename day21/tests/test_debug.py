import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter"))
from debug_decorator import debug

@debug
def multiply(a, b):
    return a * b

def test_basic():
    result = multiply(3, 4)
    assert result == 12

if __name__ == "__main__":
    test_basic()
    print("All tests passed!")