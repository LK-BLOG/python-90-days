"""字符串表示"""
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    def __str__(self):
        return f'({self.x}, {self.y})'
    def __format__(self, fmt):
        if fmt == '.2f':
            return f'({self.x:.2f}, {self.y:.2f})'
        return str(self)

p = Point(3.14159, 2.71828)
print(repr(p))      # Point(3.14159, 2.71828)
print(str(p))       # (3.14159, 2.71828)
print(f'{p:.2f}')   # (3.14, 2.72)
