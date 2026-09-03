"""Challenge 1: 图形继承链"""
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): pass
    @abstractmethod
    def perimeter(self): pass

class Circle(Shape):
    def __init__(self, radius):
        # TODO
        pass
    def area(self):
        # TODO
        pass
    def perimeter(self):
        # TODO
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        # TODO
        pass
    def area(self):
        # TODO
        pass
    def perimeter(self):
        # TODO
        pass
