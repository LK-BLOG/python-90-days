from typing import TypedDict, Optional

class UserDict(TypedDict):
    name: str
    age: int
    email: Optional[str]

user: UserDict = {"name": "Alice", "age": 30, "email": "alice@example.com"}
print(user["name"])