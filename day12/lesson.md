# Day 12 完整教学：Python包开发

## 1. 包基础
### 1.1 什么是包
**说明**：包是一个包含__init__.py文件的目录，用于组织相关模块。

**目录结构**：
```
my_package/
├── __init__.py      # 包初始化文件
├── module1.py       # 模块1
├── module2.py       # 模块2
└── subpackage/      # 子包
    ├── __init__.py
    └── module3.py
```

**示例**：
```python
# my_package/__init__.py
"""我的工具包"""

from .module1 import func1
from .module2 import func2

__version__ = "1.0.0"
__author__ = "张三"

# my_package/module1.py
"""模块1"""
def func1():
    return "Function 1"

# my_package/module2.py
"""模块2"""
def func2():
    return "Function 2"

# 使用包
import my_package
print(my_package.func1())
print(my_package.func2())
print(my_package.__version__)
```

### 1.2 __init__.py的作用
**说明**：__init__.py是包的初始化文件，在导入包时执行。

**用途**：
1. 标识目录为Python包
2. 控制导出的接口
3. 执行初始化代码
4. 定义包级别的变量

**示例**：
```python
# my_package/__init__.py
"""我的工具包"""

# 导入公共接口
from .core import MyClass
from .utils import helper_function

# 定义包级别变量
__version__ = "1.0.0"
__all__ = ['MyClass', 'helper_function']

# 初始化代码
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("my_package 已加载")
```

## 2. 包结构设计
### 2.1 标准包结构
**推荐结构**：
```
my_package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── subpackage/
│           ├── __init__.py
│           └── module.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── docs/
│   └── README.md
├── pyproject.toml
├── setup.py
├── README.md
└── LICENSE
```

**示例**：
```python
# 创建包结构
from pathlib import Path

def create_package_structure(package_name):
    """创建包结构"""
    dirs = [
        f"{package_name}/src/{package_name}",
        f"{package_name}/tests",
        f"{package_name}/docs",
    ]
    
    files = [
        f"{package_name}/src/{package_name}/__init__.py",
        f"{package_name}/src/{package_name}/core.py",
        f"{package_name}/src/{package_name}/utils.py",
        f"{package_name}/tests/__init__.py",
        f"{package_name}/pyproject.toml",
        f"{package_name}/README.md",
    ]
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    for f in files:
        Path(f).touch()

# 创建示例包
create_package_structure("my_awesome_package")
```

### 2.2 模块划分原则
**原则**：
1. 单一职责：每个模块只做一件事
2. 高内聚：相关功能放在同一模块
3. 低耦合：模块间依赖最小化
4. 清晰接口：只暴露必要的API

**示例**：
```python
# my_package/
# ├── __init__.py      # 包接口
# ├── models.py        # 数据模型
# ├── services.py      # 业务逻辑
# ├── utils.py         # 工具函数
# └── exceptions.py    # 异常定义

# my_package/__init__.py
from .models import User, Product
from .services import UserService, ProductService
from .exceptions import ValidationError, NotFoundError

# my_package/models.py
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# my_package/services.py
class UserService:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)

class ProductService:
    def __init__(self):
        self.products = []

# my_package/utils.py
def validate_email(email):
    return "@" in email

# my_package/exceptions.py
class ValidationError(Exception):
    pass

class NotFoundError(Exception):
    pass
```

## 3. 导入方式
### 3.1 绝对导入
**说明**：使用完整的模块路径导入。

**语法**：
```python
# 绝对导入
import my_package.module1
from my_package import module2
from my_package.module1 import func1
```

**示例**：
```python
# 绝对导入示例
import my_package.core
from my_package import utils
from my_package.models import User

# 使用
user = User("张三", "zhangsan@example.com")
result = utils.validate_email(user.email)
```

### 3.2 相对导入
**说明**：使用相对路径导入，适合包内部使用。

**语法**：
```python
# 相对导入
from . import module  # 同级目录
from .module import func  # 同级目录的模块
from .. import module  # 父目录
from ..module import func  # 父目录的模块
```

**示例**：
```python
# my_package/subpackage/module.py
from . import helper  # 相对导入同级模块
from .. import core  # 相对导入父包模块
from ..models import User  # 相对导入父包的模块

def func():
    helper.do_something()
    user = User("test", "test@example.com")
```

### 3.3 导入最佳实践
**建议**：
1. 包内部使用相对导入
2. 外部使用绝对导入
3. 避免循环导入
4. 使用__all__控制导出

**示例**：
```python
# my_package/__init__.py
# 使用绝对导入，导出公共接口
from .core import MyClass
from .utils import helper_function

__all__ = ['MyClass', 'helper_function']

# my_package/core.py
# 使用相对导入，导入包内模块
from .utils import helper_function
from .models import Model

class MyClass:
    def __init__(self):
        self.model = Model()
```

## 4. 包配置文件
### 4.1 pyproject.toml
**说明**：现代Python包的配置文件。

**示例**：
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my_package"
version = "1.0.0"
description = "我的Python工具包"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "张三", email = "zhangsan@example.com"}
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "black>=21.0.0",
    "flake8>=3.9.0",
]

[project.urls]
Homepage = "https://github.com/zhangsan/my_package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/zhangsan/my_package"

[tool.setuptools.packages.find]
where = ["src"]
```

### 4.2 setup.py（传统方式）
**说明**：传统的包配置文件。

**示例**：
```python
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="1.0.0",
    description="我的Python工具包",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="张三",
    author_email="zhangsan@example.com",
    url="https://github.com/zhangsan/my_package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

### 4.3 依赖管理
**说明**：管理包的依赖关系。

**示例**：
```python
# requirements.txt
requests>=2.25.0
click>=8.0.0
pandas>=1.3.0

# requirements-dev.txt
-r requirements.txt
pytest>=6.0.0
black>=21.0.0
flake8>=3.9.0

# 使用pip安装依赖
# pip install -r requirements.txt
# pip install -r requirements-dev.txt
```

## 5. 命名空间包
### 5.1 什么是命名空间包
**说明**：允许包名在不同位置分布。

**用途**：
1. 大型项目分割
2. 多团队协作
3. 插件系统

**示例**：
```python
# 命名空间包结构
# company.packageA/
# company.packageB/
# company.packageC/

# 每个子包可以独立安装
# pip install company-packageA
# pip install company-packageB

# 使用时自动合并
import company.packageA
import company.packageB
```

### 5.2 创建命名空间包
**示例**：
```python
# 不需要__init__.py
# 直接创建目录结构

# package_a/
# └── my_namespace/
#     └── module_a.py

# package_b/
# └── my_namespace/
#     └── module_b.py

# 安装后可以这样使用
from my_namespace import module_a
from my_namespace import module_b
```

## 6. 包发布
### 6.1 构建包
**命令**：
```bash
# 安装构建工具
pip install build

# 构建包
python -m build

# 生成的文件在dist/目录
```

### 6.2 发布到PyPI
**步骤**：
1. 注册PyPI账号
2. 安装twine：`pip install twine`
3. 上传：`twine upload dist/*`

**示例**：
```bash
# 构建
python -m build

# 检查包
twine check dist/*

# 上传到测试PyPI
twine upload --repository testpypi dist/*

# 上传到正式PyPI
twine upload dist/*
```

## 7. 实际应用：创建工具包
```python
# my_toolkit/
# ├── __init__.py
# ├── string_tools.py
# ├── file_tools.py
# └── data_tools.py

# my_toolkit/__init__.py
"""我的工具包"""

from .string_tools import *
from .file_tools import *
from .data_tools import *

__version__ = "1.0.0"
__author__ = "张三"

# my_toolkit/string_tools.py
"""字符串工具"""

__all__ = ['capitalize_words', 'reverse_string', 'truncate']

def capitalize_words(text):
    """每个单词首字母大写"""
    return text.title()

def reverse_string(text):
    """反转字符串"""
    return text[::-1]

def truncate(text, max_length=100, suffix="..."):
    """截断字符串"""
    if len(text) <= max_length:
        return text
    return text[:max_length-len(suffix)] + suffix

# my_toolkit/file_tools.py
"""文件工具"""

__all__ = ['read_file', 'write_file', 'file_exists']

from pathlib import Path

def read_file(filename, encoding='utf-8'):
    """读取文件"""
    return Path(filename).read_text(encoding=encoding)

def write_file(filename, content, encoding='utf-8'):
    """写入文件"""
    Path(filename).write_text(content, encoding=encoding)

def file_exists(filename):
    """检查文件是否存在"""
    return Path(filename).exists()

# my_toolkit/data_tools.py
"""数据工具"""

__all__ = ['flatten_list', 'chunk_list', 'merge_dicts']

def flatten_list(nested_list):
    """展平嵌套列表"""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

def chunk_list(lst, chunk_size):
    """分割列表"""
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def merge_dicts(*dicts):
    """合并字典"""
    result = {}
    for d in dicts:
        result.update(d)
    return result

# 使用工具包
from my_toolkit import capitalize_words, read_file, flatten_list

# 使用字符串工具
text = "hello world"
print(capitalize_words(text))  # Hello World

# 使用文件工具
if file_exists("test.txt"):
    content = read_file("test.txt")
    print(content)

# 使用数据工具
nested = [[1, 2], [3, 4], [5, 6]]
flat = flatten_list(nested)
print(flat)  # [1, 2, 3, 4, 5, 6]
```

## 8. 常见错误与调试
1. **导入错误**：检查包结构和__init__.py
2. **循环导入**：重构代码或使用延迟导入
3. **依赖缺失**：检查requirements.txt
4. **版本冲突**：使用虚拟环境
5. **打包错误**：检查pyproject.toml配置

## 9. 动手练习
1. 创建自己的工具包
2. 设计合理的包结构
3. 添加单元测试
4. 编写文档
5. 发布到PyPI

---
**掌握包开发，让你的代码更具价值！**
