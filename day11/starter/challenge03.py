# Day 11 - Challenge 3: 模块化 Todo 系统
# 难度: ⭐⭐⭐☆☆
#
# 要求: 将 Todo 系统拆分为多个模块：数据模型、存储、管理器、CLI
# 参考 challenge.md

"""
模块化 Todo 系统挑战 — 将一个完整系统拆分为职责清晰的模块

模块划分:
- models: Todo 数据模型
- storage: JSON 存储层
- manager: 业务逻辑层
- cli: 命令行交互层
"""

import json
from datetime import datetime


# ===== models 模块模拟 =====
class Todo:
    """待办事项数据模型

    Attributes:
        id: 唯一标识
        title: 标题
        done: 是否完成
        created_at: 创建时间
    """

    def __init__(self, title: str, todo_id: int = 0, done: bool = False):
        # TODO: 初始化各属性，设置 created_at 为当前时间
        pass

    def mark_done(self) -> None:
        """标记为已完成"""
        # TODO: 设置 done = True
        pass

    def to_dict(self) -> dict:
        """序列化为字典"""
        # TODO: 返回 {"id": ..., "title": ..., "done": ..., "created_at": ...}
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """从字典反序列化

        Args:
            data: 包含 Todo 字段的字典

        Returns:
            Todo 实例
        """
        # TODO: 从 data 构造 Todo 对象
        pass

    def __repr__(self) -> str:
        status = "✅" if self.done else "⏳"
        # TODO: 返回 "[✅/⏳] #id title"
        pass


# ===== storage 模块模拟 =====
class JsonStorage:
    """JSON 文件存储

    负责 Todo 的持久化，将数据保存到 JSON 文件。
    """

    def __init__(self, filepath: str = "todos.json"):
        # TODO: 设置文件路径
        pass

    def save(self, todos: list) -> None:
        """保存 Todo 列表到文件

        Args:
            todos: Todo 实例列表
        """
        # TODO: 将 todos 转为字典列表，写入 JSON 文件
        pass

    def load(self) -> list:
        """从文件加载 Todo 列表

        Returns:
            Todo 实例列表（文件不存在则返回空列表）
        """
        # TODO: 读取 JSON 文件，转为 Todo 列表
        pass


# ===== manager 模块模拟 =====
class TodoManager:
    """Todo 业务管理器

    提供增删改查的高层 API。
    """

    def __init__(self, storage: JsonStorage = None):
        # TODO: 初始化存储和 todo 列表
        pass

    def add(self, title: str) -> Todo:
        """添加新 Todo

        Args:
            title: 待办标题

        Returns:
            新创建的 Todo
        """
        # TODO: 创建 Todo -> 加入列表 -> 保存 -> 返回
        pass

    def complete(self, todo_id: int) -> bool:
        """完成指定 Todo

        Args:
            todo_id: Todo ID

        Returns:
            是否成功完成
        """
        # TODO: 查找对应 id 的 Todo，标记完成并保存
        pass

    def remove(self, todo_id: int) -> bool:
        """删除指定 Todo"""
        # TODO: 从列表中移除并保存
        pass

    def list_all(self, show_done: bool = True) -> list:
        """列出所有 Todo"""
        # TODO: 返回 todo 列表（可选过滤已完成的）
        pass

    def summary(self) -> dict:
        """统计摘要

        Returns:
            {"total": ..., "done": ..., "pending": ...}
        """
        # TODO: 统计总数、已完成数、待完成数
        pass


# ===== cli 模块模拟（简单版） =====
def print_menu():
    """打印菜单"""
    # TODO: 打印操作菜单
    print("1. 添加  2. 完成  3. 删除  4. 列表  5. 统计  0. 退出")


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 模块化 Todo 系统测试 ===")

    storage = JsonStorage("test_todos.json")
    mgr = TodoManager(storage)

    # 添加
    t1 = mgr.add("学习 Python 模块系统")
    t2 = mgr.add("完成挑战")
    print(t1, t2)

    # 完成
    mgr.complete(t1.id)

    # 列表
    for t in mgr.list_all():
        print(t)

    # 统计
    print(mgr.summary())

    print("✅ Challenge 03 完成")
