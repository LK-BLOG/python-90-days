# Day 7 挑战一：基础 Todo 类 (★★★☆☆)
# 要求: 创建 Todo 数据类，包含属性、序列化、验证。


import json
from datetime import datetime


class Todo:
    """单个待办事项。
    
    属性:
        id (int): 唯一标识符
        title (str): 标题（必填）
        description (str): 描述（可选）
        priority (str): 优先级 "高"/"中"/"低"
        tags (list): 标签列表
        completed (bool): 完成状态
        created_at (str): 创建时间 ISO 格式
        completed_at (str|None): 完成时间
    """
    
    VALID_PRIORITIES = ("高", "中", "低")
    _next_id = 1  # 类变量：自增ID
    
    def __init__(self, title, description="", priority="中",
                 tags=None, completed=False):
        """初始化 Todo。
        
        Args:
            title: 标题（必填，空字符串会抛 ValueError）
            description: 描述
            priority: 优先级
            tags: 标签列表
            completed: 初始完成状态
        """
        # TODO: 生成自增ID
        # TODO: 验证 title 非空
        # TODO: 验证 priority 在合法范围内
        # TODO: 初始化所有属性
        pass
    
    def complete(self):
        """标记为已完成，记录完成时间。"""
        # TODO: 设置 completed=True, completed_at=当前时间
        pass
    
    def uncomplete(self):
        """取消完成状态。"""
        pass
    
    def add_tag(self, tag):
        """添加标签（去重）。"""
        pass
    
    def remove_tag(self, tag):
        """移除标签。"""
        pass
    
    def to_dict(self):
        """转为字典（用于 JSON 序列化）。"""
        # TODO: 返回所有属性的字典
        pass
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建 Todo（反序列化）。"""
        # TODO: 从字典重建 Todo 对象，恢复所有字段
        pass
    
    @classmethod
    def from_json(cls, json_str):
        """从 JSON 字符串创建 Todo。"""
        pass
    
    def to_json(self):
        """转为 JSON 字符串。"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def __repr__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} [{self.id}] {self.title} ({self.priority})"


# ===== 测试 =====
if __name__ == "__main__":
    t = Todo("学习Python", "完成Day7", priority="高", tags=["学习", "编程"])
    print(f"创建: {t}")
    
    t.complete()
    print(f"完成: {t}")
    
    d = t.to_dict()
    t2 = Todo.from_dict(d)
    print(f"反序列化: {t2}")
    print(f"JSON:\n{t.to_json()}")
