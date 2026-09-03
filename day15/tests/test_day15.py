"""Day 15 测试"""
def test_property():
    class Temp:
        def __init__(self, c):
            self._c = c
        @property
        def celsius(self): return self._c
        @celsius.setter
        def celsius(self, v):
            if v < -273.15: raise ValueError('Below absolute zero')
            self._c = v
        @property
        def fahrenheit(self): return self._c * 9/5 + 32
    t = Temp(100)
    assert t.fahrenheit == 212.0
    t.celsius = 0
    assert t.fahrenheit == 32.0

def test_private():
    class Secret:
        def __init__(self): self.__data = 'hidden'
        def get_data(self): return self.__data
    s = Secret()
    assert s.get_data() == 'hidden'
    assert hasattr(s, '_Secret__data')

def test_classmethod_factory():
    class Box:
        def __init__(self, w, h):
            self.w, self.h = w, h
        @classmethod
        def square(cls, s): return cls(s, s)
    b = Box.square(10)
    assert b.w == b.h == 10

if __name__ == '__main__':
    test_property()
    test_private()
    test_classmethod_factory()
    print('All Day 15 tests passed!')
