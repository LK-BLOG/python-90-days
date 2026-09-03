from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    age: int
    scores: list = field(default_factory=list)
    # TODO: __post_init__ 计算 average_score

s = Student('Alice', 20, [90, 85, 92])
