# challenge01/starter.py - 基础Todo类骨架
# 请根据README要求完善这个文件

from datetime import datetime

class Todo:
    """Todo类，用于表示单个任务"""
    
    def __init__(self, title, description="", priority="中", tags=None):
        """
        初始化Todo
        
        参数:
            title (str): 标题，必填
            description (str): 描述，可选
            priority (str): 优先级，可选（高/中/低）
            tags (list): 标签列表，可选
        """
        # TODO: 实现输入验证
        # 验证标题不为空
        # 验证标题长度
        # 验证优先级值
        
        # TODO: 初始化属性
        # 设置id为None（稍后设置）
        # 设置标题、描述、优先级、标签
        # 设置默认值
        
        pass
    
    def complete(self):
        """标记为已完成"""
        # TODO: 设置completed为True
        # TODO: 设置completed_at为当前时间
        pass
    
    def to_dict(self):
        """转换为字典，用于JSON序列化"""
        # TODO: 返回包含所有属性的字典
        # 确保时间格式正确
        pass
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建Todo实例
        
        参数:
            data (dict): 包含Todo数据的字典
        
        返回:
            Todo: Todo实例
        """
        # TODO: 从字典中提取数据
        # TODO: 创建Todo实例
        # TODO: 设置所有属性
        # TODO: 处理时间格式
        pass
    
    def __str__(self):
        """字符串表示"""
        # TODO: 返回友好的字符串表示
        # 包含状态图标、优先级图标、标题
        # 格式: [状态] 优先级图标 标题
        pass

# 测试代码
if __name__ == "__main__":
    # 测试1: 创建Todo
    try:
        todo1 = Todo("学习Python", "完成Day7项目", "高", ["学习", "编程"])
        print(f"创建成功: {todo1}")
        
        # 测试2: 转换为字典
        todo_dict = todo1.to_dict()
        print(f"字典表示: {todo_dict}")
        
        # 测试3: 从字典恢复
        todo2 = Todo.from_dict(todo_dict)
        print(f"恢复成功: {todo2}")
        
        # 测试4: 完成功能
        todo1.complete()
        print(f"完成状态: {todo1}")
        
        # 验证
        assert todo1.title == todo2.title
        assert todo1.priority == todo2.priority
        assert todo1.completed == True
        
        print("所有测试通过！")
        
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"未预期的错误: {e}")
