"""物品系统"""
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
    description: str = ''
    value: int = 0

    def use(self, character):
        raise NotImplementedError

    def __repr__(self):
        return f'Item({self.name})'

@dataclass
class Weapon(Item):
    attack_bonus: int = 0
    item_type: ItemType = field(default=ItemType.WEAPON, init=False)

@dataclass
class Armor(Item):
    defense_bonus: int = 0
    item_type: ItemType = field(default=ItemType.ARMOR, init=False)

@dataclass
class Potion(Item):
    heal_amount: int = 50
    item_type: ItemType = field(default=ItemType.CONSUMABLE, init=False)

    def use(self, character):
        old_hp = character.hp
        character.hp = min(character.max_hp, character.hp + self.heal_amount)
        healed = character.hp - old_hp
        return f'{character.name} 使用 {self.name}，恢复 {healed} HP'
