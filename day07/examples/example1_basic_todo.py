# 示例1：基础Todo类
# 展示函数参数设计、字符串处理、异常处理

from datetime import datetime

class Todo:
    """Todo类，展示函数参数设计"""
    
    def __init__(self, title, description="", priority="中", tags=None):
        """
        初始化Todo
        
        参数:
            title (str): 标题，必填
            description (str): 描述，可选
            priority (str): 优先级，可选（高/中/低）
            tags (list): 标签列表，可选
        """
        # 输入验证
        if not title or not title.strip():
            raise ValueError("标题不能为空")
        if len(title) > 100:
            raise ValueError("标题不能超过100个字符")
        
        valid_priorities = ["高", "中", "低"]
        if priority not in valid_priorities:
            raise ValueError(f"优先级必须是: {', '.join(valid_priorities)}")
        
        # 初始化属性
        self.id = None  # 稍后设置
        self.title = title.strip()
        self.description = description.strip()
        self.priority = priority
        self.tags = tags if tags is not None else []
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None
    
    def complete(self):
        """标记为已完成"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def to_dict(self):
        """转换为字典，用于JSON序列化"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "tags": self.tags,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建Todo实例"""
        todo = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "中"),
            tags=data.get("tags", [])
        )
        todo.id = data.get("id")
        todo.completed = data.get("completed", False)
        if data.get("created_at"):
            todo.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("completed_at"):
            todo.completed_at = datetime.fromisoformat(data["completed_at"])
        return todo
    
    def __str__(self):
        """字符串表示"""
        status = "✓" if self.completed else "✗"
        priority_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(self.priority, "⚪")
        return f"[{status}] {priority_icon} {self.title}"

# 测试代码
if __name__ == "__main__":
    try:
        # 创建Todo
        todo1 = Todo("学习Python", "完成Day7项目", "高", ["学习", "编程"])
        print(f"创建成功: {todo1}")
        
        # 转换为字典
        todo_dict = todo1.to_dict()
        print(f"字典表示: {todo_dict}")
        
        # 从字典恢复
        todo2 = Todo.from_dict(todo_dict)
        print(f"恢复成功: {todo2}")
        
        # 验证属性
        assert todo1.title == todo2.title
        assert todo1.priority == todo2.priority
        print("所有测试通过！")
        
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"未预期的错误: {e}")
