from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def __init__(self, r): self.r = r
    def draw(self): return "O" * self.r

class Square:
    def __init__(self, s): self.s = s
    def draw(self): return "\n".join(["X" * self.s] * self.s)

def render(obj: Drawable):
    print(obj.draw())

render(Circle(3))
render(Square(3))
