"""角色系统"""
from abc import ABC, abstractmethod

class Stat:
    def __init__(self, min_val=0, max_val=999):
        self.min_val, self.max_val = min_val, max_val
    def __set_name__(self, owner, name):
        self.attr = f'_stat_{name}'
    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.attr, 0)
    def __set__(self, obj, value):
        setattr(obj, self.attr, max(self.min_val, min(self.max_val, value)))

class Character(ABC):
    hp = Stat(0, 999)
    mp = Stat(0, 999)
    attack = Stat(1, 999)
    defense = Stat(0, 999)

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.equipment = {'weapon': None, 'armor': None}
        self._attack_bonus = 0
        self._defense_bonus = 0

    @property
    @abstractmethod
    def max_hp(self): pass

    @property
    @abstractmethod
    def max_mp(self): pass

    @abstractmethod
    def attack_action(self, target): pass

    def take_damage(self, damage):
        actual = max(0, damage - self.defense - self._defense_bonus)
        self.hp = max(0, self.hp - actual)
        return actual

    def is_alive(self):
        return self.hp > 0

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, HP={self.hp}/{self.max_hp})'

class Warrior(Character):
    @property
    def max_hp(self): return 100 + self.level * 20
    @property
    def max_mp(self): return 30 + self.level * 5

    def attack_action(self, target):
        damage = 15 + self.level * 3 + self._attack_bonus
        actual = target.take_damage(damage)
        return f'{self.name} 挥剑攻击 {target.name}，造成 {actual} 伤害'

class Mage(Character):
    @property
    def max_hp(self): return 60 + self.level * 10
    @property
    def max_mp(self): return 80 + self.level * 15

    def attack_action(self, target):
        if self.mp < 10:
            return '魔力不足!'
        self.mp -= 10
        damage = 25 + self.level * 5 + self._attack_bonus
        actual = target.take_damage(damage)
        return f'{self.name} 释放火球术，对 {target.name} 造成 {actual} 伤害'
