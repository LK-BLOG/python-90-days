"""Day 14 测试用例"""
from abc import ABC, abstractmethod

def test_abc():
    class Shape(ABC):
        @abstractmethod
        def area(self): pass
    class Circle(Shape):
        def __init__(self, r): self.r = r
        def area(self): return 3.14 * self.r ** 2
    c = Circle(5)
    assert abs(c.area() - 78.5) < 1

def test_mro():
    class A:
        def show(self): return 'A'
    class B(A):
        def show(self): return 'B'
    class C(A):
        def show(self): return 'C'
    class D(B, C):
        pass
    assert D().show() == 'B'
    assert [c.__name__ for c in D.__mro__] == ['D', 'B', 'C', 'A', 'object']

def test_isinstance():
    class Animal: pass
    class Dog(Animal): pass
    d = Dog()
    assert isinstance(d, Dog)
    assert isinstance(d, Animal)
    assert issubclass(Dog, Animal)

def test_mixin():
    class JsonMixin:
        def to_dict(self):
            return self.__dict__.copy()
    class User(JsonMixin):
        def __init__(self, name): self.name = name
    u = User('Alice')
    assert u.to_dict() == {'name': 'Alice'}

if __name__ == '__main__':
    test_abc()
    test_mro()
    test_isinstance()
    test_mixin()
    print('All Day 14 tests passed!')
