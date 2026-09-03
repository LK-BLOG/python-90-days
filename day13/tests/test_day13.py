"""Day 13 测试用例"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_class_attribute():
    """测试类属性 vs 实例属性"""
    class Counter:
        count = 0
        def __init__(self):
            Counter.count += 1
    c1, c2 = Counter()
    assert Counter.count == 2
    assert c1.count == 2
    del c1
    # count 是类属性，del实例不影响

def test_classmethod():
    """测试类方法工厂"""
    class Box:
        def __init__(self, w, h):
            self.w, self.h = w, h
        @classmethod
        def square(cls, size):
            return cls(size, size)
    b = Box.square(10)
    assert b.w == 10 and b.h == 10

def test_staticmethod():
    """测试静态方法"""
    class Math:
        @staticmethod
        def add(a, b):
            return a + b
    assert Math.add(3, 4) == 7

def test_descriptor():
    """测试描述符验证"""
    class Positive:
        def __set_name__(self, owner, name):
            self.name = name
        def __get__(self, obj, objtype=None):
            if obj is None: return self
            return obj.__dict__.get(self.name, 0)
        def __set__(self, obj, value):
            if value < 0:
                raise ValueError(f'{self.name} must be positive')
            obj.__dict__[self.name] = value

    class Item:
        price = Positive()
        def __init__(self, price):
            self.price = price

    item = Item(10)
    assert item.price == 10
    try:
        item.price = -1
        assert False, "Should raise ValueError"
    except ValueError:
        pass

def test_slots():
    """测试 __slots__"""
    class Point:
        __slots__ = ('x', 'y')
        def __init__(self, x, y):
            self.x, self.y = x, y
    p = Point(1, 2)
    assert p.x == 1 and p.y == 2
    assert not hasattr(p, '__dict__')

def test_singleton():
    """测试单例模式"""
    class Singleton:
        _instance = None
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
    a, b = Singleton(), Singleton()
    assert a is b

if __name__ == '__main__':
    test_class_attribute()
    test_classmethod()
    test_staticmethod()
    test_descriptor()
    test_slots()
    test_singleton()
    print('All Day 13 tests passed!')
