from dataclasses import dataclass, field

@dataclass
class Department:
    name: str
    budget: float

@dataclass
class Employee:
    name: str
    age: int
    department: Department
    # TODO: to_dict() 方法
