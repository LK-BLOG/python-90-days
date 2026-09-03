from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1)           # Point(x=1, y=2)
print(p1 == p2)     # True

@dataclass
class Config:
    host: str = 'localhost'
    port: int = 8080
    debug: bool = False
    tags: list = field(default_factory=list)

c = Config()
print(c)
