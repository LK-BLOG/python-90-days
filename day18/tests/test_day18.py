"""Day 18 测试"""
def test_character_creation():
    from abc import ABC
    # 测试角色创建
    class MockChar:
        def __init__(self, name, hp):
            self.name = name
            self.hp = hp
    c = MockChar('Hero', 100)
    assert c.name == 'Hero'
    assert c.hp == 100

def test_inventory():
    class Inv:
        def __init__(self, cap=5):
            self._items, self._cap = [], cap
        def __len__(self): return len(self._items)
        def __contains__(self, i): return i in self._items
        def add(self, i):
            if len(self._items) >= self._cap: raise ValueError('full')
            self._items.append(i)
    inv = Inv()
    inv.add('sword')
    inv.add('shield')
    assert len(inv) == 2
    assert 'sword' in inv

def test_item_dataclass():
    from dataclasses import dataclass, field
    from enum import Enum
    class ItemType(Enum):
        WEAPON = 'weapon'
        POTION = 'potion'
    @dataclass
    class Item:
        name: str
        item_type: ItemType
        value: int = 0
    sword = Item('Iron Sword', ItemType.WEAPON, 100)
    assert sword.name == 'Iron Sword'
    assert sword.item_type == ItemType.WEAPON

def test_stat_descriptor():
    class Stat:
        def __init__(self, lo=0, hi=999):
            self.lo, self.hi = lo, hi
        def __set_name__(self, owner, name):
            self.attr = f'_s_{name}'
        def __get__(self, obj, cls=None):
            if obj is None: return self
            return getattr(obj, self.attr, 0)
        def __set__(self, obj, val):
            setattr(obj, self.attr, max(self.lo, min(self.hi, val)))
    class Hero:
        hp = Stat(0, 100)
    h = Hero()
    h.hp = 50
    assert h.hp == 50
    h.hp = 200
    assert h.hp == 100
    h.hp = -10
    assert h.hp == 0

if __name__ == '__main__':
    test_character_creation()
    test_inventory()
    test_item_dataclass()
    test_stat_descriptor()
    print('All Day 18 tests passed!')
