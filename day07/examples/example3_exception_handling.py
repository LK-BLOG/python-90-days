# 示例3：异常处理与文件操作
# 展示异常处理、文件读写、JSON操作

import json
from pathlib import Path
from datetime import datetime

class TodoStorage:
    """Todo存储类，展示异常处理和文件操作"""
    
    def __init__(self, filename="todos.json"):
        self.filename = Path(filename)
        self.todos = []
        self.load()
    
    def load(self):
        """从文件加载数据"""
        try:
            if self.filename.exists():
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
                print(f"成功加载 {len(self.todos)} 个Todo")
            else:
                print("文件不存在，创建新的数据文件")
                self.todos = []
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print("使用空数据")
            self.todos = []
        except PermissionError:
            print("没有权限读取文件")
            self.todos = []
        except Exception as e:
            print(f"加载失败: {e}")
            self.todos = []
    
    def save(self):
        """保存数据到文件"""
        try:
            # 确保目录存在
            self.filename.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            print("数据保存成功")
            return True
        except PermissionError:
            print("没有权限写入文件")
            return False
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def add_todo(self, todo):
        """添加Todo"""
        try:
            # 验证输入
            if not isinstance(todo, dict):
                raise TypeError("Todo必须是字典类型")
            
            required_fields = ["title"]
            for field in required_fields:
                if field not in todo or not todo[field]:
                    raise ValueError(f"缺少必填字段: {field}")
            
            # 生成ID
            if self.todos:
                max_id = max(t.get("id", 0) for t in self.todos)
                todo["id"] = max_id + 1
            else:
                todo["id"] = 1
            
            # 设置默认值
            todo.setdefault("description", "")
            todo.setdefault("priority", "中")
            todo.setdefault("tags", [])
            todo.setdefault("completed", False)
            todo.setdefault("created_at", datetime.now().isoformat())
            todo.setdefault("completed_at", None)
            
            self.todos.append(todo)
            if self.save():
                return todo
            else:
                # 保存失败，从列表中移除
                self.todos.pop()
                return None
        except (TypeError, ValueError) as e:
            print(f"数据验证错误: {e}")
            return None
        except Exception as e:
            print(f"添加Todo失败: {e}")
            return None
    
    def backup(self, backup_name=None):
        """创建备份"""
        try:
            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"todos_backup_{timestamp}.json"
            
            backup_path = Path(backup_name)
            
            # 复制当前数据到备份文件
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            
            print(f"备份创建成功: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"备份失败: {e}")
            return None
    
    def restore(self, backup_file):
        """从备份恢复"""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                raise FileNotFoundError(f"备份文件不存在: {backup_file}")
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                restored_todos = json.load(f)
            
            # 验证数据格式
            if not isinstance(restored_todos, list):
                raise ValueError("备份文件格式错误")
            
            # 创建当前数据的备份
            current_backup = self.backup("current_before_restore.json")
            
            # 恢复数据
            self.todos = restored_todos
            if self.save():
                print(f"成功恢复 {len(self.todos)} 个Todo")
                return True
            else:
                # 恢复失败，尝试从当前备份恢复
                if current_backup:
                    self.restore(current_backup)
                return False
        except FileNotFoundError as e:
            print(f"文件未找到: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"备份文件格式错误: {e}")
            return False
        except Exception as e:
            print(f"恢复失败: {e}")
            return False

def safe_input(prompt, input_type=str, default=None):
    """安全的用户输入函数"""
    while True:
        try:
            user_input = input(f"{prompt}" + (f" [{default}]" if default is not None else "") + ": ").strip()
            
            if not user_input and default is not None:
                return default
            
            if not user_input and default is None:
                print("输入不能为空，请重新输入")
                continue
            
            return input_type(user_input)
        except ValueError:
            print(f"输入格式错误，请输入{input_type.__name__}类型")
        except KeyboardInterrupt:
            print("\n操作已取消")
            raise
        except EOFError:
            print("\n输入结束")
            raise

# 测试代码
if __name__ == "__main__":
    # 创建临时存储
    storage = TodoStorage("test_todos.json")
    
    # 添加测试数据
    test_todos = [
        {"title": "任务1", "priority": "高", "tags": ["学习"]},
        {"title": "任务2", "priority": "中", "tags": ["工作"]},
        {"title": "任务3", "priority": "低", "tags": ["生活"]}
    ]
    
    for todo in test_todos:
        result = storage.add_todo(todo)
        if result:
            print(f"添加成功: {result['title']}")
        else:
            print(f"添加失败: {todo['title']}")
    
    # 测试备份
    backup_path = storage.backup()
    
    # 测试搜索
    print("\n搜索包含'任务'的Todo:")
    found = [t for t in storage.todos if "任务" in t["title"]]
    for t in found:
        print(f"  - {t['title']}")
    
    # 清理测试文件
    import os
    if os.path.exists("test_todos.json"):
        os.remove("test_todos.json")
    if backup_path and os.path.exists(backup_path):
        os.remove(backup_path)
    
    print("\n所有测试完成！")
