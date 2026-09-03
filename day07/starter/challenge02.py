# Day 7 挑战二：Todo 管理器 (★★★☆☆)
# 要求: 实现增删改查、持久化、统计。


import json
import os
from datetime import datetime


class TodoManager:
    """Todo 管理器 —— 管理 Todo 集合，支持 CRUD 和持久化。"""
    
    def __init__(self, filepath="todos.json"):
        """初始化管理器。
        
        Args:
            filepath: 数据存储文件路径
        """
        self.filepath = filepath
        self._todos = []       # Todo 列表
        self._counter = 0      # ID 计数器
        self._op_count = 0     # 操作计数（闭包示例）
    
    def add(self, title, description="", priority="中", tags=None):
        """添加 Todo。"""
        # TODO: 创建 Todo 对象，加入列表，自增ID
        # TODO: 自动保存
        pass
    
    def delete(self, todo_id):
        """按 ID 删除 Todo。"""
        # TODO: 查找并删除，找不到抛 ValueError
        pass
    
    def get(self, todo_id):
        """按 ID 获取 Todo。"""
        pass
    
    def update(self, todo_id, **kwargs):
        """更新 Todo 的指定字段。"""
        # TODO: 支持更新 title, description, priority, tags
        pass
    
    def complete(self, todo_id):
        """标记完成。"""
        pass
    
    def search(self, keyword):
        """按关键词搜索（标题+描述模糊匹配）。"""
        # TODO: 遍历搜索
        pass
    
    def filter_by(self, priority=None, completed=None, tag=None):
        """按条件过滤。"""
        pass
    
    def get_stats(self):
        """返回统计信息。"""
        # TODO: 统计总数、已完成、各优先级数量、标签频率
        pass
    
    def save(self):
        """保存到 JSON 文件。"""
        # TODO: 将所有 Todo 序列化并写入文件
        pass
    
    def load(self):
        """从 JSON 文件加载。"""
        # TODO: 读取文件，重建 Todo 列表
        pass
    
    @property
    def operation_count(self):
        """用闭包实现的操作计数器。"""
        pass
    
    def __len__(self):
        return len(self._todos)
    
    def __iter__(self):
        return iter(self._todos)


# ===== 测试 =====
if __name__ == "__main__":
    mgr = TodoManager("_test_todos.json")
    mgr.add("学习Python", priority="高", tags=["学习"])
    mgr.add("买菜", priority="低")
    mgr.add("写代码", priority="高", tags=["编程", "工作"])
    
    print(f"总数: {len(mgr)}")
    mgr.complete(1)
    print(f"统计: {mgr.get_stats()}")
    
    for t in mgr:
        print(f"  {t}")
    
    mgr.save()
    mgr.load()
    print(f"重新加载后: {len(mgr)} 条")
    
    # 清理测试文件
    if os.path.exists("_test_todos.json"):
        os.remove("_test_todos.json")
