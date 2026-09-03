from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        # TODO: 初始化 HP, MP

    @property
    @abstractmethod
    def max_hp(self): pass

    @property
    @abstractmethod
    def max_mp(self): pass

    @abstractmethod
    def attack_action(self, target): pass

    def is_alive(self):
        # TODO
        pass

class Warrior(Character):
    @property
    def max_hp(self):
        # TODO: 高 HP
        pass
    @property
    def max_mp(self):
        # TODO: 低 MP
        pass
    def attack_action(self, target):
        # TODO: 物理攻击
        pass

class Mage(Character):
    @property
    def max_hp(self): pass
    @property
    def max_mp(self): pass
    def attack_action(self, target): pass
