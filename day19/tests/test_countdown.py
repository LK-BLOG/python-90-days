import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter"))
from countdown import Countdown

def test_countdown_basic():
    assert list(Countdown(5)) == [5, 4, 3, 2, 1]

def test_countdown_one():
    assert list(Countdown(1)) == [1]

def test_countdown_zero():
    assert list(Countdown(0)) == []

if __name__ == "__main__":
    test_countdown_basic()
    test_countdown_one()
    test_countdown_zero()
    print("All tests passed!")