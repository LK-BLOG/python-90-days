# Day 7 完整教学：CLI Todo管理器

## 1. 项目概述
我们将构建一个命令行交互式Todo管理器，综合运用前六天所学知识。这个项目将帮助你理解如何将零散的知识点组合成实际应用。

## 2. 需求分析
### 功能需求：
- 添加Todo（标题、描述、优先级）
- 查看所有Todo
- 搜索和过滤Todo
- 编辑Todo
- 删除Todo
- 统计信息
- 数据持久化（JSON文件）

### 技术需求：
- 函数参数设计：不同函数需要不同的参数组合
- 闭包：用于计数器、日志记录
- 字符串处理：格式化输出、输入验证
- 数据结构：列表存储Todo，字典表示Todo对象
- 异常处理：文件操作、用户输入验证

## 3. 知识点回顾与应用

### 3.1 函数参数设计
**应用场景**：Todo函数需要灵活的参数组合
```python
# 示例：添加Todo函数
def add_todo(title, description="", priority="中", tags=None):
    """添加Todo，支持可选参数"""
    if tags is None:
        tags = []
    todo = {
        "title": title,
        "description": description,
        "priority": priority,
        "tags": tags,
        "completed": False
    }
    return todo

# 使用示例
todo1 = add_todo("学习Python")  # 使用默认值
todo2 = add_todo("完成作业", "完成Day7挑战", "高", ["学习", "编程"])
```

**常见错误**：
- 忘记设置可变默认值（如`tags=[]`应该用`tags=None`然后在函数内初始化）
- 参数顺序错误：有默认值的参数必须放在后面

### 3.2 闭包的应用
**应用场景**：Todo计数器、操作日志
```python
# Todo计数器闭包
def create_todo_counter():
    """创建Todo计数器闭包"""
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    def get_count():
        return count
    
    return increment, get_count

# 使用示例
increment, get_count = create_todo_counter()
print(f"添加第{increment()}个Todo")  # 添加第1个Todo
print(f"添加第{increment()}个Todo")  # 添加第2个Todo
print(f"当前总数: {get_count()}")    # 当前总数: 2
```

**操作日志闭包**：
```python
def create_operation_logger():
    """创建操作日志闭包"""
    operations = []
    
    def log_operation(operation_type, todo_title):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        operations.append({
            "time": timestamp,
            "type": operation_type,
            "todo": todo_title
        })
        return f"[{timestamp}] {operation_type}: {todo_title}"
    
    def get_operations():
        return operations.copy()  # 返回副本，防止外部修改
    
    def clear_operations():
        operations.clear()
    
    return log_operation, get_operations, clear_operations

# 使用示例
log, get_ops, clear_ops = create_operation_logger()
print(log("添加", "学习Python"))
print(log("完成", "买菜"))
print(f"操作记录: {get_ops()}")
```

### 3.3 字符串处理
**应用场景**：格式化输出Todo、验证输入
```python
# Todo格式化输出
def format_todo(todo, index=None):
    """格式化Todo输出"""
    status = "✓" if todo["completed"] else "✗"
    priority_colors = {"高": "🔴", "中": "🟡", "低": "🟢"}
    priority_icon = priority_colors.get(todo["priority"], "⚪")
    
    header = f"[{status}] {priority_icon} {todo['title']}"
    if index is not None:
        header = f"{index}. {header}"
    
    lines = [header]
    if todo["description"]:
        lines.append(f"   描述: {todo['description']}")
    if todo["tags"]:
        lines.append(f"   标签: {', '.join(todo['tags'])}")
    
    return "\n".join(lines)

# 使用示例
todo = {
    "title": "学习Python",
    "description": "完成Day7项目",
    "priority": "高",
    "tags": ["学习", "编程"],
    "completed": False
}
print(format_todo(todo, 1))
```

**输入验证**：
```python
def validate_todo_input(title, priority=None):
    """验证Todo输入"""
    errors = []
    
    # 验证标题
    if not title or not title.strip():
        errors.append("标题不能为空")
    elif len(title) > 100:
        errors.append("标题不能超过100个字符")
    
    # 验证优先级
    if priority is not None:
        valid_priorities = ["高", "中", "低"]
        if priority not in valid_priorities:
            errors.append(f"优先级必须是: {', '.join(valid_priorities)}")
    
    return errors

# 使用示例
errors = validate_todo_input("", "高")
print(errors)  # ['标题不能为空']
errors = validate_todo_input("学习Python", "紧急")
print(errors)  # ['优先级必须是: 高, 中, 低']
```

### 3.4 数据结构操作
**应用场景**：Todo列表管理、搜索过滤
```python
# Todo管理器类
class TodoManager:
    def __init__(self):
        self.todos = []
    
    def add_todo(self, todo):
        """添加Todo"""
        self.todos.append(todo)
    
    def get_completed_count(self):
        """获取已完成Todo数量"""
        return len([t for t in self.todos if t["completed"]])
    
    def get_by_priority(self, priority):
        """按优先级筛选"""
        return [t for t in self.todos if t["priority"] == priority]
    
    def search_todos(self, keyword):
        """搜索Todo"""
        keyword = keyword.lower()
        results = []
        for todo in self.todos:
            if (keyword in todo["title"].lower() or 
                keyword in todo["description"].lower()):
                results.append(todo)
        return results
    
    def get_statistics(self):
        """获取统计信息"""
        total = len(self.todos)
        completed = self.get_completed_count()
        pending = total - completed
        
        # 按优先级统计
        priority_stats = {}
        for priority in ["高", "中", "低"]:
            count = len(self.get_by_priority(priority))
            priority_stats[priority] = count
        
        return {
            "总数": total,
            "已完成": completed,
            "待完成": pending,
            "优先级分布": priority_stats
        }

# 使用示例
manager = TodoManager()
manager.add_todo({"title": "任务1", "priority": "高", "completed": False})
manager.add_todo({"title": "任务2", "priority": "中", "completed": True})
print(manager.get_statistics())
```

### 3.5 异常处理
**应用场景**：文件操作、用户输入处理
```python
# JSON文件操作
import json
from pathlib import Path

def save_todos(todos, filename="todos.json"):
    """保存Todo到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)
        return True
    except PermissionError:
        print(f"错误: 没有权限写入文件 {filename}")
        return False
    except Exception as e:
        print(f"保存失败: {e}")
        return False

def load_todos(filename="todos.json"):
    """从JSON文件加载Todo"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件 {filename} 不存在，将创建新文件")
        return []
    except json.JSONDecodeError:
        print(f"文件 {filename} 格式错误")
        return []
    except Exception as e:
        print(f"加载失败: {e}")
        return []

# 用户输入处理
def get_user_input(prompt, input_type=str, default=None):
    """获取用户输入，支持类型转换和默认值"""
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
        except Exception as e:
            print(f"输入错误: {e}")
```

## 4. 完整项目实现

### 4.1 主程序结构
```python
# todo_app.py - 主程序
import json
from datetime import datetime
from pathlib import Path

class TodoApp:
    def __init__(self, data_file="todos.json"):
        self.data_file = Path(data_file)
        self.todos = []
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.todos = []
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def add_todo(self, title, description="", priority="中", tags=None):
        """添加Todo"""
        if tags is None:
            tags = []
        
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "tags": tags,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None
        }
        
        self.todos.append(todo)
        if self.save_data():
            return todo
        return None
    
    def list_todos(self, show_completed=True):
        """列出所有Todo"""
        if not show_completed:
            return [t for t in self.todos if not t["completed"]]
        return self.todos
    
    def search_todos(self, keyword):
        """搜索Todo"""
        keyword = keyword.lower()
        return [t for t in self.todos 
                if keyword in t["title"].lower() or 
                keyword in t["description"].lower() or
                any(keyword in tag.lower() for tag in t["tags"])]
    
    def update_todo(self, todo_id, **kwargs):
        """更新Todo"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                for key, value in kwargs.items():
                    if key in todo:
                        todo[key] = value
                if self.save_data():
                    return todo
        return None
    
    def delete_todo(self, todo_id):
        """删除Todo"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                deleted = self.todos.pop(i)
                if self.save_data():
                    return deleted
        return None
    
    def get_statistics(self):
        """获取统计信息"""
        total = len(self.todos)
        completed = len([t for t in self.todos if t["completed"]])
        pending = total - completed
        
        # 按优先级统计
        priorities = {"高": 0, "中": 0, "低": 0}
        for todo in self.todos:
            if todo["priority"] in priorities:
                priorities[todo["priority"]] += 1
        
        # 按日期统计
        date_stats = {}
        for todo in self.todos:
            date = todo["created_at"].split()[0]
            date_stats[date] = date_stats.get(date, 0) + 1
        
        return {
            "总数": total,
            "已完成": completed,
            "待完成": pending,
            "优先级分布": priorities,
            "日期分布": date_stats
        }
```

### 4.2 用户界面
```python
def print_menu():
    """打印主菜单"""
    print("\n" + "="*50)
    print("📋 Todo管理器")
    print("="*50)
    print("1. 添加Todo")
    print("2. 查看所有Todo")
    print("3. 搜索Todo")
    print("4. 编辑Todo")
    print("5. 删除Todo")
    print("6. 统计信息")
    print("7. 退出")
    print("="*50)

def main():
    """主函数"""
    app = TodoApp()
    
    while True:
        print_menu()
        choice = input("请选择操作 (1-7): ").strip()
        
        if choice == "1":
            # 添加Todo
            title = input("标题: ").strip()
            if not title:
                print("标题不能为空")
                continue
            
            description = input("描述 (可选): ").strip()
            
            while True:
                priority = input("优先级 (高/中/低) [中]: ").strip() or "中"
                if priority in ["高", "中", "低"]:
                    break
                print("优先级必须是: 高, 中, 低")
            
            tags_input = input("标签 (用逗号分隔，可选): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
            
            todo = app.add_todo(title, description, priority, tags)
            if todo:
                print(f"✅ Todo添加成功！ID: {todo['id']}")
            else:
                print("❌ 添加失败")
        
        elif choice == "2":
            # 查看所有Todo
            show_completed = input("是否显示已完成的Todo? (y/n) [y]: ").strip().lower() != 'n'
            todos = app.list_todos(show_completed)
            
            if not todos:
                print("没有找到Todo")
                continue
            
            print(f"\n找到 {len(todos)} 个Todo:")
            for todo in todos:
                status = "✓" if todo["completed"] else "✗"
                priority_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(todo["priority"], "⚪")
                print(f"  {todo['id']}. [{status}] {priority_icon} {todo['title']}")
                if todo["description"]:
                    print(f"      描述: {todo['description']}")
                print(f"      创建时间: {todo['created_at']}")
        
        elif choice == "3":
            # 搜索Todo
            keyword = input("搜索关键词: ").strip()
            if not keyword:
                print("关键词不能为空")
                continue
            
            results = app.search_todos(keyword)
            if not results:
                print(f"没有找到包含 '{keyword}' 的Todo")
                continue
            
            print(f"\n找到 {len(results)} 个匹配的Todo:")
            for todo in results:
                status = "✓" if todo["completed"] else "✗"
                print(f"  {todo['id']}. [{status}] {todo['title']}")
        
        elif choice == "4":
            # 编辑Todo
            try:
                todo_id = int(input("要编辑的Todo ID: ").strip())
            except ValueError:
                print("请输入有效的ID")
                continue
            
            todo = next((t for t in app.todos if t["id"] == todo_id), None)
            if not todo:
                print(f"未找到ID为 {todo_id} 的Todo")
                continue
            
            print(f"当前Todo: {todo['title']}")
            print("（直接回车保持原值）")
            
            new_title = input(f"新标题 [{todo['title']}]: ").strip()
            new_desc = input(f"新描述 [{todo['description']}]: ").strip()
            new_priority = input(f"新优先级 [{todo['priority']}]: ").strip()
            
            updates = {}
            if new_title:
                updates["title"] = new_title
            if new_desc:
                updates["description"] = new_desc
            if new_priority and new_priority in ["高", "中", "低"]:
                updates["priority"] = new_priority
            
            if updates:
                updated = app.update_todo(todo_id, **updates)
                if updated:
                    print("✅ 更新成功")
                else:
                    print("❌ 更新失败")
            else:
                print("没有需要更新的内容")
        
        elif choice == "5":
            # 删除Todo
            try:
                todo_id = int(input("要删除的Todo ID: ").strip())
            except ValueError:
                print("请输入有效的ID")
                continue
            
            confirm = input(f"确定要删除ID为 {todo_id} 的Todo吗? (y/n): ").strip().lower()
            if confirm == 'y':
                deleted = app.delete_todo(todo_id)
                if deleted:
                    print(f"✅ 已删除: {deleted['title']}")
                else:
                    print(f"❌ 未找到ID为 {todo_id} 的Todo")
        
        elif choice == "6":
            # 统计信息
            stats = app.get_statistics()
            print("\n📊 统计信息:")
            print(f"  总数: {stats['总数']}")
            print(f"  已完成: {stats['已完成']}")
            print(f"  待完成: {stats['待完成']}")
            print("  优先级分布:")
            for priority, count in stats["优先级分布"].items():
                icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(priority, "⚪")
                print(f"    {icon} {priority}: {count}")
        
        elif choice == "7":
            print("👋 再见！")
            break
        
        else:
            print("无效的选择，请输入1-7")

if __name__ == "__main__":
    main()
```

## 5. 测试用例
```python
# test_todo.py
import unittest
from todo_app import TodoApp
import tempfile
import os

class TestTodoApp(unittest.TestCase):
    def setUp(self):
        """测试前设置"""
        self.test_file = tempfile.mktemp(suffix='.json')
        self.app = TodoApp(self.test_file)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_todo(self):
        """测试添加Todo"""
        todo = self.app.add_todo("测试任务", "测试描述", "高", ["测试"])
        self.assertIsNotNone(todo)
        self.assertEqual(todo["title"], "测试任务")
        self.assertEqual(todo["priority"], "高")
        self.assertEqual(todo["tags"], ["测试"])
        self.assertFalse(todo["completed"])
    
    def test_list_todos(self):
        """测试列出Todo"""
        self.app.add_todo("任务1")
        self.app.add_todo("任务2")
        todos = self.app.list_todos()
        self.assertEqual(len(todos), 2)
    
    def test_search_todos(self):
        """测试搜索Todo"""
        self.app.add_todo("学习Python")
        self.app.add_todo("买菜")
        results = self.app.search_todos("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "学习Python")
    
    def test_update_todo(self):
        """测试更新Todo"""
        todo = self.app.add_todo("原始标题")
        updated = self.app.update_todo(todo["id"], title="新标题")
        self.assertEqual(updated["title"], "新标题")
    
    def test_delete_todo(self):
        """测试删除Todo"""
        todo = self.app.add_todo("要删除的任务")
        deleted = self.app.delete_todo(todo["id"])
        self.assertEqual(deleted["title"], "要删除的任务")
        self.assertEqual(len(self.app.todos), 0)
    
    def test_statistics(self):
        """测试统计功能"""
        self.app.add_todo("高优先级", priority="高")
        self.app.add_todo("中优先级", priority="中")
        self.app.add_todo("低优先级", priority="低")
        stats = self.app.get_statistics()
        self.assertEqual(stats["总数"], 3)
        self.assertEqual(stats["优先级分布"]["高"], 1)

if __name__ == "__main__":
    unittest.main()
```

## 6. 常见错误与调试
1. **文件路径问题**：使用`pathlib.Path`处理路径
2. **编码问题**：始终指定`encoding='utf-8'`
3. **JSON序列化**：确保所有数据都是JSON可序列化的
4. **ID管理**：使用自增ID，删除后不要重用
5. **状态管理**：completed字段应该是布尔值

## 7. 扩展功能
- 添加截止日期
- 子任务支持
- 数据导出（CSV、Markdown）
- 彩色输出
- 命令行参数支持

## 8. 动手练习
1. 完成所有功能的实现
2. 添加数据验证
3. 实现统计图表（使用字符绘制）
4. 添加撤销/重做功能
5. 实现数据备份和恢复

---
**提示**：今天的项目是后续几天的基础，请确保代码质量！
