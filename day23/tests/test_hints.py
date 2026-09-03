import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter"))

def test_basic():
    from type_hints import add, get_first, find_max
    assert add(1, 2) == 3
    assert get_first([1, 2, 3]) == 1
    assert find_max([1, 5, 3]) == 5
    assert find_max([]) is None

if __name__ == "__main__":
    test_basic()
    print("All tests passed!")