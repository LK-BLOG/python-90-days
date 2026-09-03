# Basic type hints

def greet(name: str) -> str:
    return f"Hello, {name}"

age: int = 25
scores: list[int] = [90, 85, 95]
config: dict[str, str] = {"key": "value"}

print(greet("Alice"))
print(f"Scores: {scores}")