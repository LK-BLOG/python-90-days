from dataclasses import dataclass

@dataclass
class Circle:
    radius: float
    area: float = 0.0

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError('半径不能为负')
        self.area = 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)  # 78.54
