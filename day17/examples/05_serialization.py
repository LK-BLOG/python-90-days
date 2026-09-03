from dataclasses import dataclass, asdict
import json

@dataclass
class User:
    name: str
    age: int
    scores: list = None

u = User('Alice', 25, [90, 85])
d = asdict(u)
print(d)
print(json.dumps(d, ensure_ascii=False, indent=2))
