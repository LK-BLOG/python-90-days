import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter"))
from gen_range import gen_range

def test_basic():
    assert list(gen_range(5)) == [0,1,2,3,4]

def test_start_stop():
    assert list(gen_range(2, 5)) == [2,3,4]

def test_step():
    assert list(gen_range(0, 10, 2)) == [0,2,4,6,8]

if __name__ == "__main__":
    test_basic()
    test_start_stop()
    test_step()
    print("All tests passed!")