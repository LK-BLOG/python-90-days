from dataclasses import dataclass, field
from enum import Enum

class ItemType(Enum):
    WEAPON = 'weapon'
    ARMOR = 'armor'
    CONSUMABLE = 'consumable'

@dataclass
class Item:
    name: str
    item_type: ItemType
    value: int = 0

@dataclass
class Weapon(Item):
    attack_bonus: int = 0
    # TODO: equip() 方法

@dataclass
class Potion(Item):
    heal_amount: int = 50
    # TODO: use() 方法
