# __slots__ 内存优化

import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlotPoint:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

rp = RegularPoint(1, 2)
sp = SlotPoint(1, 2)

print(f'RegularPoint dict: {sys.getsizeof(rp.__dict__)} bytes')
# SlotPoint 没有 __dict__，节省内存
print(f'Has __dict__: {hasattr(rp, "__dict__")} {hasattr(sp, "__dict__")}')
# True False

# 继承中的 slots
class Base:
    __slots__ = ('x',)
class Child(Base):
    __slots__ = ('y',)

c = Child()
c.x = 1
c.y = 2
print(c.x, c.y)
