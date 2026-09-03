"""Challenge 4: 接口检查系统"""
from abc import ABC, abstractmethod

class Flyable(ABC):
    @abstractmethod
    def fly(self): pass

class Swimmable(ABC):
    @abstractmethod
    def swim(self): pass

# TODO: 创建 Duck 同时实现 Flyable 和 Swimmable
# TODO: 创建 Penguin 只实现 Swimmable
# TODO: 检查类型并调用方法
