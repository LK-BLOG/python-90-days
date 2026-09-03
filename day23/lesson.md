# Day 23: Type System

## 1. Type Hints Basics
```python
# Function annotations
def greet(name: str) -> str:
    return f"Hello, {name}"

# Variable annotations
age: int = 25
name: str = "Alice"
```

## 2. Built-in Types
```python
# Python 3.9+ uses built-in generics
numbers: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1, "b": 2}
nested: list[dict[str, int]] = [{"x": 1}, {"y": 2}]
coordinates: tuple[int, int, int] = (1, 2, 3)
unique: set[str] = {"a", "b", "c"}
```

## 3. Optional and Union
```python
from typing import Optional, Union

# Optional[X] = Union[X, None]
def find_user(user_id: int) -> Optional[dict]:
    if user_id > 0:
        return {"id": user_id}
    return None

# Union - multiple types
def process(value: Union[str, int]) -> str:
    return str(value)

# Python 3.10+: use |
def process_v2(value: str | int) -> str:
    return str(value)
```

## 4. TypeVar (Generics)
```python
from typing import TypeVar, Sequence

T = TypeVar("T")

def first(lst: Sequence[T]) -> T:
    return lst[0]

# Bounded TypeVar
from typing import TypeVar
Numeric = TypeVar("Numeric", int, float)

def add(a: Numeric, b: Numeric) -> Numeric:
    return a + b
```

## 5. Protocol (Structural Subtyping)
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Circle"

class Square:
    def draw(self) -> str:
        return "Square"

def render(shape: Drawable) -> str:
    return shape.draw()

# Both work - no inheritance needed
render(Circle())  # OK
render(Square())  # OK
```

## 6. TYPE_CHECKING
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from my_module import MyClass  # Only imported at type check time

def process(obj: "MyClass") -> None:
    pass  # Forward reference
```

## 7. TypedDict
```python
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int
    email: Optional[str]

user: UserDict = {"name": "Alice", "age": 30}  # email is optional
```

## 8. Callable and Iterable
```python
from typing import Callable, Iterable

def apply(func: Callable[[int], int], values: Iterable[int]) -> list[int]:
    return [func(v) for v in values]

# Callable[[args], return_type]
# Iterable[int] - any iterable of ints
```

## 9. Final, Literal, Annotated
```python
from typing import Final, Literal, Annotated

MAX_SIZE: Final = 100  # Cannot be reassigned

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    pass

# Annotated - add metadata
from typing import Annotated
UserId = Annotated[int, "Must be positive"]

def get_user(user_id: UserId) -> str:
    return f"User {user_id}"
```

## 10. mypy Basics
```bash
# Install
pip install mypy

# Check a file
mypy myfile.py

# Check a project
mypy src/
```

### Common mypy errors
- Incompatible types in assignment
- Missing return statement
- Argument has incompatible type
- Name "x" is not defined

## 11. Type-Safe Design Patterns
```python
# Builder pattern with types
class QueryBuilder:
    def __init__(self):
        self._table: str = ""
        self._conditions: list[str] = []
        self._limit: Optional[int] = None

    def table(self, name: str) -> "QueryBuilder":
        self._table = name
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> str:
        sql = f"SELECT * FROM {self._table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        if self._limit:
            sql += f" LIMIT {self._limit}"
        return sql
```

## Exercises
1. Add type hints to existing functions
2. Create a Protocol for a plugin system
3. Use TypeVar to create a generic stack class