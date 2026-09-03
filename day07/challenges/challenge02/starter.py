# challenge02/starter.py - Todo管理器骨架
import json
from pathlib import Path

class TodoManager:
    """Todo管理器，提供CRUD操作和数据持久化"""
    
    def __init__(self, data_file="todos.json"):
        """
        初始化管理器
        
        参数:
            data_file (str): 数据文件路径
        """
        # TODO: 初始化数据文件路径
        # TODO: 初始化Todo列表
        # TODO: 加载现有数据
        pass
    
    def load_data(self):
        """从JSON文件加载数据"""
        # TODO: 检查文件是否存在
        # TODO: 读取JSON文件
        # TODO: 解析JSON数据
        # TODO: 处理异常情况
        pass
    
    def save_data(self):
        """保存数据到JSON文件"""
        # TODO: 确保目录存在
        # TODO: 将数据转换为JSON格式
        # TODO: 写入文件
        # TODO: 处理异常情况
        pass
    
    def add_todo(self, title, description="", priority="中", tags=None):
        """添加Todo"""
        # TODO: 创建Todo字典
        # TODO: 生成ID
        # TODO: 添加到列表
        # TODO: 保存数据
        # TODO: 返回创建的Todo
        pass
    
    def list_todos(self, show_completed=True):
        """列出所有Todo"""
        # TODO: 根据参数过滤Todo
        # TODO: 返回Todo列表
        pass
    
    def search_todos(self, keyword):
        """搜索Todo"""
        # TODO: 在标题、描述、标签中搜索
        # TODO: 返回匹配的Todo列表
        pass
    
    def update_todo(self, todo_id, **kwargs):
        """更新Todo"""
        # TODO: 根据ID查找Todo
        # TODO: 更新指定字段
        # TODO: 保存数据
        # TODO: 返回更新后的Todo
        pass
    
    def delete_todo(self, todo_id):
        """删除Todo"""
        # TODO: 根据ID查找Todo
        # TODO: 从列表中移除
        # TODO: 保存数据
        # TODO: 返回被删除的Todo
        pass
    
    def get_statistics(self):
        """获取统计信息"""
        # TODO: 计算总数
        # TODO: 计算已完成数量
        # TODO: 按优先级统计
        # TODO: 返回统计字典
        pass

# 测试代码
if __name__ == "__main__":
    # 创建管理器
    manager = TodoManager("test_manager.json")
    
    # 添加测试数据
    todo1 = manager.add_todo("任务1", "描述1", "高", ["标签1"])
    todo2 = manager.add_todo("任务2", "描述2", "中", ["标签2"])
    
    print(f"添加成功: {todo1}")
    print(f"添加成功: {todo2}")
    
    # 测试搜索
    results = manager.search_todos("任务")
    print(f"找到 {len(results)} 个匹配的Todo")
    
    # 测试统计
    stats = manager.get_statistics()
    print(f"统计信息: {stats}")
    
    # 清理
    import os
    if os.path.exists("test_manager.json"):
        os.remove("test_manager.json")
