"""property 完整用法"""
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError('半径不能为负')
        self._radius = value

    @property
    def area(self):  # 只读
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.area)  # 78.54
c.radius = 10  # OK
# c.area = 100  # AttributeError
