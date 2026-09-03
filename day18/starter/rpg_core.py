# ============================================================
# Day 18 骨架代码：RPG 游戏核心框架
# ============================================================
# 这是 RPG 游戏的类骨架。你需要根据 challenge 要求实现所有方法。
# 每个类都有 TODO 标记，按顺序完成即可。
# ============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


# ---------- 装备/物品基类 ----------

@dataclass
class Item:
    """游戏物品基类"""
    name: str
    description: str
    value: int  # 价值/价格

    # TODO: 实现 __repr__，格式: Item(name, value)
    def __repr__(self):
        pass

    # TODO: 实现 __eq__，按 name 判断相等
    def __eq__(self, other):
        pass


@dataclass
class Weapon(Item):
    """武器"""
    damage: int = 0
    attack_speed: float = 1.0

    # TODO: 实现属性 attack_power → damage * attack_speed
    @property
    def attack_power(self):
        pass


@dataclass
class Armor(Item):
    """防具"""
    defense: int = 0
    durability: int = 100

    # TODO: 实现方法 absorb(damage) → 返回实际受到的伤害
    def absorb(self, damage):
        pass


@dataclass
class Consumable(Item):
    """消耗品（药水等）"""
    heal_amount: int = 0
    quantity: int = 1

    # TODO: 实现 use(target) → 回复目标HP
    def use(self, target):
        pass


# ---------- 角色系统 ----------

@dataclass
class Character:
    """角色基类"""
    name: str
    hp: int = 100
    max_hp: int = 100
    mp: int = 50
    max_mp: int = 50
    level: int = 1
    exp: int = 0
    attack: int = 10
    defense: int = 5

    # TODO: 实现 is_alive 属性 → hp > 0
    @property
    def is_alive(self):
        pass

    # TODO: 实现 take_damage(amount) → 扣减HP，不低于0
    def take_damage(self, amount):
        pass

    # TODO: 实现 heal(amount) → 回复HP，不超过 max_hp
    def heal(self, amount):
        pass

    # TODO: 实现 attack_target(target) → 造成 damage - target.defense 的伤害
    def attack_target(self, target):
        pass

    # TODO: 实现 gain_exp(amount) → 增加经验，满100升级
    def gain_exp(self, amount):
        pass

    # TODO: 实现 level_up() → 升级逻辑
    def level_up(self):
        pass

    # TODO: 实现 __str__，格式: "角色名 Lv.1 HP:100/100"
    def __str__(self):
        pass


# ---------- 背包系统 ----------

class Inventory:
    """背包系统"""

    def __init__(self, capacity=20):
        # TODO: 初始化背包，self.items = [], self.capacity = capacity
        pass

    # TODO: 实现 __len__ → 返回物品数量
    def __len__(self):
        pass

    # TODO: 实现 __contains__ → 判断物品是否在背包中
    def __contains__(self, item):
        pass

    # TODO: 实现 __getitem__ → 按索引获取物品
    def __getitem__(self, index):
        pass

    # TODO: 实现 add(item) → 添加物品，满了抛异常
    def add(self, item):
        pass

    # TODO: 实现 remove(item) → 移除物品
    def remove(self, item):
        pass

    # TODO: 实现 find_by_name(name) → 按名字查找物品
    def find_by_name(self, name):
        pass

    # TODO: 实现 get_by_type(item_type) → 按类型筛选物品
    def get_by_type(self, item_type):
        pass

    # TODO: 实现 sort_by_value() → 按价值排序
    def sort_by_value(self):
        pass


# ---------- 战斗系统 ----------

class Combat:
    """回合制战斗系统"""

    def __init__(self, player, enemy):
        # TODO: 初始化战斗双方
        pass

    # TODO: 实现 is_over → 战斗是否结束
    @property
    def is_over(self):
        pass

    # TODO: 实现 player_turn(action) → 玩家回合
    # action: "attack", "defend", "use_item", "flee"
    def player_turn(self, action, **kwargs):
        pass

    # TODO: 实现 enemy_turn() → 敌方AI回合
    def enemy_turn(self):
        pass

    # TODO: 实现 run() → 运行完整战斗流程
    def run(self):
        pass

    # TODO: 实现 get_battle_log() → 返回战斗日志
    def get_battle_log(self):
        pass


# ---------- 测试入口 ----------

if __name__ == "__main__":
    print("=== RPG 游戏核心框架 - 骨架代码 ===")
    print("请根据 challenge.md 要求实现所有 TODO 方法")
    print()

    # 基础测试
    sword = Weapon("铁剑", "一把普通的铁剑", 50, damage=15, attack_speed=1.2)
    shield = Armor("木盾", "一个结实的木盾", 30, defense=5)
    potion = Consumable("小血瓶", "回复20HP", 10, heal_amount=20)

    player = Character("勇者", hp=100, max_hp=100, attack=12, defense=3)
    enemy = Character("史莱姆", hp=30, max_hp=30, attack=5, defense=1)

    bag = Inventory()

    print("物品创建成功")
    print(f"武器: {sword}")
    print(f"防具: {shield}")
    print(f"消耗品: {potion}")
    print(f"玩家: {player}")
    print(f"敌人: {enemy}")
    print("请实现所有 TODO 方法后重新运行此文件")
