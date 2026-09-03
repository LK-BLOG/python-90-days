"""Boss: 图形系统 - 起手代码"""
from abc import ABC, abstractmethod
import json

class Shape(ABC):
    @abstractmethod
    def area(self): pass
    @abstractmethod
    def perimeter(self): pass
    def describe(self):
        return f'{self.__class__.__name__}: area={self.area():.2f}'

# TODO: Circle, Rectangle, Triangle 继承 Shape
# TODO: Mixin: Drawable, Serializable, Comparable
# TODO: Composite: 图形组合
# TODO: ShapeFactory: 从字符串创建
