# Day 23 Boss: RPG Type Annotations

## Project: TypedRPG

## Goal
Add complete type annotations to the RPG game framework from Day 18.

## Requirements
1. Type all dataclasses (Character, Item, Spell, etc.)
2. Type all methods and functions
3. Create TypedDict for JSON game state
4. Create Protocol for game plugins
5. Create TypeVar for generic collections
6. Type-safe event system
7. Type-safe command parser

## Type Hints to Add
```python
# Dataclass fields
class Character:
    name: str
    hp: int
    max_hp: int
    inventory: list[Item]
    stats: dict[str, int]

# Methods
def attack(self, target: "Character") -> int:
    ...

# Return types
def find_item(self, name: str) -> Optional[Item]:
    ...

# Callbacks
AttackCallback = Callable[["Character", "Character"], int]
```

## Acceptance Criteria
- All dataclass fields typed
- All method signatures typed
- TypedDict for save/load format
- Protocol for plugin interface
- TypeVar for generic Result/Either type
- All code passes mypy --strict (or close to it)

## Difficulty: 4/5