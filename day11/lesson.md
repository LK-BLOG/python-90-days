# Day 11 完整教学：模块系统

## 1. 模块基础
### 1.1 什么是模块
**说明**：模块是一个包含Python代码的文件，文件名就是模块名。

**语法**：
```python
# 创建模块：mymodule.py
def hello():
    print("Hello from module!")

# 使用模块
import mymodule
mymodule.hello()
```

**示例**：
```python
# math_utils.py
def add(a, b):
    """两数相加"""
    return a + b

def subtract(a, b):
    """两数相减"""
    return a - b

PI = 3.14159

class Calculator:
    """计算器类"""
    def multiply(self, a, b):
        return a * b

# 使用模块
import math_utils

print(math_utils.add(2, 3))  # 5
print(math_utils.PI)  # 3.14159
calc = math_utils.Calculator()
print(calc.multiply(2, 3))  # 6
```

### 1.2 导入方式
**方式**：
- `import module`：导入整个模块
- `from module import name`：导入特定名称
- `from module import *`：导入所有名称（不推荐）
- `import module as alias`：导入并重命名

**示例**：
```python
# 方式1：导入整个模块
import math
print(math.sqrt(16))

# 方式2：导入特定名称
from math import sqrt, pi
print(sqrt(16))
print(pi)

# 方式3：导入所有（不推荐）
from math import *
print(sqrt(16))

# 方式4：导入并重命名
import math as m
print(m.sqrt(16))
```

## 2. 模块搜索路径
### 2.1 sys.path
**说明**：Python搜索模块的路径列表。

**示例**：
```python
import sys
import sys

# 打印搜索路径
print("模块搜索路径:")
for path in sys.path:
    print(f"  {path}")

# 添加搜索路径
import os
custom_path = '/path/to/my/modules'
if custom_path not in sys.path:
    sys.path.append(custom_path)
```

### 2.2 模块查找顺序
**顺序**：
1. 当前目录
2. PYTHONPATH环境变量
3. 标准库目录
4. 第三方包目录

**示例**：
```python
# 查看模块来源
import os
print(f"os模块位置: {os.__file__}")

# 查看内置模块
import sys
print(f"内置模块: {sys.builtin_module_names}")
```

## 3. __name__变量
### 3.1 基础用法
**说明**：__name__变量表示模块名称。

**语法**：
```python
# 当模块被直接运行时，__name__为"__main__"
# 当模块被导入时，__name__为模块名

if __name__ == "__main__":
    # 只在直接运行时执行
    main()
```

**示例**：
```python
# calculator.py
def add(a, b):
    return a + b

def main():
    """主函数"""
    print("计算器模块")
    print(f"2 + 3 = {add(2, 3)}")

if __name__ == "__main__":
    # 直接运行时执行
    main()
else:
    # 被导入时执行
    print(f"计算器模块被导入: {__name__}")
```

### 3.2 实际应用
**示例**：
```python
# config.py
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "debug": False,
    "log_level": "INFO",
    "max_connections": 10
}

def load_config(config_file="config.json"):
    """加载配置文件"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG.copy()

def main():
    """主函数"""
    config = load_config()
    print("当前配置:")
    for key, value in config.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
```

## 4. __all__变量
### 4.1 控制导出
**说明**：__all__变量定义使用`from module import *`时导出的名称。

**语法**：
```python
# module.py
__all__ = ['public_func', 'PublicClass']

def public_func():
    pass

def _private_func():
    pass

class PublicClass:
    pass

class _PrivateClass:
    pass
```

**示例**：
```python
# mymodule.py
__all__ = ['add', 'subtract', 'Calculator']

def add(a, b):
    """公开函数"""
    return a + b

def subtract(a, b):
    """公开函数"""
    return a - b

def _helper():
    """私有函数（不导出）"""
    pass

class Calculator:
    """公开类"""
    pass

class _InternalCalculator:
    """私有类（不导出）"""
    pass

# 使用
from mymodule import *
# 只能访问 add, subtract, Calculator
```

## 5. 包 vs 模块
### 5.1 包结构
**说明**：包是一个包含__init__.py文件的目录。

**目录结构**：
```
mypackage/
├── __init__.py
├── module1.py
├── module2.py
└── subpackage/
    ├── __init__.py
    └── module3.py
```

**示例**：
```python
# mypackage/__init__.py
from .module1 import func1
from .module2 import func2

# mypackage/module1.py
def func1():
    return "Function 1"

# mypackage/module2.py
def func2():
    return "Function 2"

# 使用
from mypackage import func1, func2
print(func1())
print(func2())
```

### 5.2 相对导入
**语法**：
```python
# 同一包内
from . import module
from .module import func

# 父包
from .. import module
from ..module import func
```

**示例**：
```python
# mypackage/subpackage/module3.py
from . import helper  # 相对导入同级模块
from .. import module1  # 相对导入父包模块

def func3():
    helper.do_something()
    module1.func1()
```

## 6. 循环导入问题
### 6.1 问题描述
**说明**：两个模块互相导入，导致导入失败。

**问题代码**：
```python
# module_a.py
import module_b

def func_a():
    return module_b.func_b()

# module_b.py
import module_a

def func_b():
    return module_a.func_a()  # 错误！
```

### 6.2 解决方案
**方案1**：重构代码
```python
# 将公共函数移到第三个模块
# common.py
def shared_func():
    pass

# module_a.py
from common import shared_func

# module_b.py
from common import shared_func
```

**方案2**：延迟导入
```python
# module_a.py
def func_a():
    import module_b  # 延迟导入
    return module_b.func_b()
```

**方案3**：使用__name__
```python
# module_a.py
if __name__ == "__main__":
    # 只在直接运行时导入
    import module_b
```

## 7. 模块重载
### 7.1 基础重载
**说明**：使用importlib.reload()重新加载模块。

**语法**：
```python
import importlib
import mymodule

# 修改模块后重新加载
importlib.reload(mymodule)
```

**示例**：
```python
import importlib
import math_utils

print(math_utils.add(2, 3))

# 假设修改了math_utils.py
importlib.reload(math_utils)

print(math_utils.add(2, 3))  # 使用新代码
```

## 8. 实际应用：模块化Todo系统
```python
# todo_package/
# ├── __init__.py
# ├── models.py
# ├── storage.py
# ├── manager.py
# └── cli.py

# todo_package/__init__.py
"""Todo包"""
from .models import Todo
from .storage import TodoStorage
from .manager import TodoManager

__all__ = ['Todo', 'TodoStorage', 'TodoManager']

# todo_package/models.py
"""数据模型"""
from datetime import datetime

class Todo:
    """Todo类"""
    def __init__(self, title, priority="中"):
        self.title = title
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        todo = cls(data["title"], data.get("priority", "中"))
        todo.completed = data.get("completed", False)
        todo.created_at = datetime.fromisoformat(data["created_at"])
        return todo

# todo_package/storage.py
"""数据存储"""
import json
from pathlib import Path
from .models import Todo

class TodoStorage:
    """Todo存储"""
    def __init__(self, filename="todos.json"):
        self.filename = Path(filename)
        self.todos = []
    
    def load(self):
        """加载数据"""
        if self.filename.exists():
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.todos = [Todo.from_dict(item) for item in data]
    
    def save(self):
        """保存数据"""
        data = [todo.to_dict() for todo in self.todos]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# todo_package/manager.py
"""管理器"""
from .models import Todo
from .storage import TodoStorage

class TodoManager:
    """Todo管理器"""
    def __init__(self, storage=None):
        self.storage = storage or TodoStorage()
        self.storage.load()
    
    def add_todo(self, title, priority="中"):
        """添加Todo"""
        todo = Todo(title, priority)
        self.storage.todos.append(todo)
        self.storage.save()
        return todo
    
    def list_todos(self):
        """列出所有Todo"""
        return self.storage.todos

# 使用示例
if __name__ == "__main__":
    from todo_package import TodoManager
    
    manager = TodoManager()
    todo = manager.add_todo("学习模块系统")
    print(f"添加成功: {todo.title}")
```

## 9. 常见错误与调试
1. **模块未找到**：检查sys.path和模块位置
2. **循环导入**：重构代码或延迟导入
3. **导入错误**：检查模块语法
4. **命名冲突**：使用import as重命名
5. **相对导入错误**：确保包结构正确

## 10. 动手练习
1. 创建自己的工具模块
2. 实现模块化项目结构
3. 解决循环导入问题
4. 创建插件系统
5. 实现动态导入

---
**提示**：模块系统是组织代码的关键，掌握它能让你的代码更易维护！
