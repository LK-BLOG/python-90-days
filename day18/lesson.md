# Day 18: RPG 游戏核心框架 — 综合教程

## 前言
本日是 Day 13-17 的综合实战。我们将构建一个 RPG 游戏框架，用到所有 OOP 高级特性。

---

## 1. 核心类设计

### 1.1 属性描述符（Day 13, 15）

```python
from dataclasses import dataclass, field

class Stat:
    """角色属性描述符，自动限制范围"""
    def __init__(self, min_val=0, max_val=999):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.name, 0)

    def __set__(self, obj, value):
        value = max(self.min_val, min(self.max_val, value))
        setattr(obj, self.name, value)

class Character:
    hp = Stat(0, 999)
    mp = Stat(0, 999)
    attack = Stat(1, 999)
    defense = Stat(0, 999)

    def __init__(self, name, hp, mp, attack, defense):
        self.name = name
        self.hp = hp
        self.mp = mp
        self攻击力 = attack
        self.defense = defense
```

### 1.2 继承体系（Day 14）

```python
from abc import ABC, abstractmethod

class Character(ABC):
    """角色抽象基类"""

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self._hp = self.max_hp
        self._mp = self.max_mp

    @property
    @abstractmethod
    def max_hp(self): pass

    @property
    @abstractmethod
    def max_mp(self): pass

    @abstractmethod
    def attack_action(self, target): pass

    @abstractmethod
    def special_action(self, target): pass

    def is_alive(self):
        return self._hp > 0

class Warrior(Character):
    @property
    def max_hp(self): return 100 + self.level * 20

    @property
    def max_mp(self): return 30 + self.level * 5

    def attack_action(self, target):
        damage = 15 + self.level * 3
        target.take_damage(damage)
        return f'{self.name} 挥剑攻击，造成 {damage} 伤害'

    def special_action(self, target):
        if self._mp >= 10:
            self._mp -= 10
            damage = 30 + self.level * 5
            target.take_damage(damage)
            return f'{self.name} 使用旋风斩，造成 {damage} 伤害!'
        return '魔力不足!'
```

### 1.3 物品系统

```python
from dataclasses import dataclass
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

@dataclass
class Weapon(Item):
    attack_bonus: int = 0
    item_type: ItemType = ItemType.WEAPON

    def equip(self, character):
        character.equipment['weapon'] = self
        character._attack_bonus += self attack_bonus

@dataclass
class Potion(Item):
    heal_amount: int = 50
    item_type: ItemType = ItemType.CONSUMABLE

    def use(self, character):
        character._hp = min(character.max_hp, character._hp + self.heal_amount)
        return f'{character.name} 使用 {self.name}，恢复 {self.heal_amount} HP'
```

### 1.4 背包系统

```python
class Inventory:
    """背包系统 - 支持容器协议"""

    def __init__(self, capacity=20):
        self._items = []
        self._capacity = capacity

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def add(self, item):
        if len(self._items) >= self._capacity:
            raise ValueError('背包已满')
        self._items.append(item)

    def remove(self, item):
        self._items.remove(item)

    def get_by_type(self, item_type):
        return [i for i in self._items if i.item_type == item_type]
```

### 1.5 魔术方法应用（Day 16）

```python
@dataclass
class DamageResult:
    """伤害结果 - 支持运算符"""
    raw_damage: int
    actual_damage: int
    is_critical: bool = False

    def __add__(self, other):
        return DamageResult(
            self.raw_damage + other.raw_damage,
            self.actual_damage + other.actual_damage,
            self.is_critical or other.is_critical
        )

    def __str__(self):
        crit = ' (暴击!)' if self.is_critical else ''
        return f'{self.actual_damage} 伤害{crit}'

    def __bool__(self):
        return self.actual_damage > 0
```

### 1.6 任务系统

```python
from dataclasses import dataclass, field
from enum import Enum

class QuestStatus(Enum):
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

@dataclass
class Quest:
    name: str
    description: str
    objectives: list = field(default_factory=list)
    rewards: dict = field(default_factory=dict)
    status: QuestStatus = QuestStatus.NOT_STARTED

    def start(self):
        self.status = QuestStatus.IN_PROGRESS

    def complete(self):
        self.status = QuestStatus.COMPLETED
        return self.rewards
```

---

## 本日总结

这个 RPG 框架综合运用了：
- **Day 13**: 描述符（Stat）、类属性、组合
- **Day 14**: ABC（Character）、继承（Warrior/Mage）、Mixin
- **Day 15**: property、封装、工厂方法
- **Day 16**: 魔术方法（比较、容器、字符串表示）
- **Day 17**: dataclass（Item、Quest）
