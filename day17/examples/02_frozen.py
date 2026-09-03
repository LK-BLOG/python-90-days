from dataclasses import dataclass

@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

red = Color(255, 0, 0)
# red.r = 100  # FrozenInstanceError
colors = {red, Color(255, 0, 0)}
print(len(colors))  # 1
