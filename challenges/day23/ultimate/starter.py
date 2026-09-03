from typing import TypedDict, Protocol, TypeVar, Generic, Optional
from dataclasses import dataclass, field

# TODO: Add type annotations to all classes

@dataclass
class Item:
    name: str  # already typed
    value: int
    description: str
    # TODO: add more fields with types

@dataclass
class Character:
    name: str
    hp: int
    max_hp: int
    attack_power: int
    defense: int
    inventory: list
    # TODO: type inventory properly

    def take_damage(self, damage):
        pass  # TODO: add types

    def heal(self, amount):
        pass  # TODO: add types

    def is_alive(self):
        pass  # TODO: add types

class GameState(TypedDict):
    pass  # TODO: define game save format

class Plugin(Protocol):
    name: str
    def on_turn_start(self, character: Character) -> None: ...

# Generic Result type
T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T, E]):
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error

    def is_ok(self) -> bool:
        return self.error is None

# Test
if __name__ == "__main__":
    player = Character("Hero", 100, 100, 15, 5, [])
    print(player.is_alive())
    player.take_damage(30)
    print(player.hp)