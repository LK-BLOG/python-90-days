# 示例：包开发基础
from pathlib import Path
import shutil

# 创建示例包结构
def create_example_package():
    """创建示例包"""
    package_name = "example_toolkit"
    
    # 创建目录结构
    dirs = [
        package_name,
        f"{package_name}/subpackage",
        "tests",
    ]
    
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    
    # 创建__init__.py
    init_content = '''"""示例工具包"""

__version__ = "1.0.0"
__author__ = "张三"

from .core import MyClass
from .utils import helper_function

__all__ = ['MyClass', 'helper_function']
'''
    (Path(package_name) / "__init__.py").write_text(init_content, encoding='utf-8')
    
    # 创建core.py
    core_content = '''"""核心模块"""

class MyClass:
    """示例类"""
    
    def __init__(self, value):
        self.value = value
    
    def process(self):
        """处理数据"""
        return f"处理: {self.value}"
'''
    (Path(package_name) / "core.py").write_text(core_content, encoding='utf-8')
    
    # 创建utils.py
    utils_content = '''"""工具模块"""

def helper_function(text):
    """辅助函数"""
    return text.upper()
'''
    (Path(package_name) / "utils.py").write_text(utils_content, encoding='utf-8')
    
    # 创建子包
    sub_init = '''"""子包"""

def sub_function():
    """子包函数"""
    return "来自子包"
'''
    (Path(package_name) / "subpackage" / "__init__.py").write_text(sub_init, encoding='utf-8')
    
    # 创建测试
    test_content = '''"""测试模块"""
import unittest
from example_toolkit import MyClass, helper_function

class TestExampleToolkit(unittest.TestCase):
    def test_my_class(self):
        obj = MyClass("test")
        self.assertEqual(obj.process(), "处理: test")
    
    def test_helper_function(self):
        result = helper_function("hello")
        self.assertEqual(result, "HELLO")

if __name__ == "__main__":
    unittest.main()
'''
    (Path("tests") / "test_example.py").write_text(test_content, encoding='utf-8')
    
    # 创建pyproject.toml
    pyproject_content = '''[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "example-toolkit"
version = "1.0.0"
description = "示例工具包"
readme = "README.md"
requires-python = ">=3.8"

[project.urls]
Homepage = "https://github.com/example/example-toolkit"
'''
    Path("pyproject.toml").write_text(pyproject_content, encoding='utf-8')
    
    # 创建README.md
    readme_content = '''# 示例工具包

这是一个示例Python包，展示包开发的基础知识。

## 安装

```bash
pip install -e .
```

## 使用

```python
from example_toolkit import MyClass, helper_function

obj = MyClass("test")
print(obj.process())

result = helper_function("hello")
print(result)
```
'''
    Path("README.md").write_text(readme_content, encoding='utf-8')
    
    print(f"示例包 '{package_name}' 已创建")

# 使用示例
if __name__ == "__main__":
    # 创建示例包
    create_example_package()
    
    # 演示导入
    print("\n=== 演示导入 ===")
    import sys
    sys.path.insert(0, ".")
    
    import example_toolkit
    print(f"包版本: {example_toolkit.__version__}")
    print(f"作者: {example_toolkit.__author__}")
    
    # 使用包
    obj = example_toolkit.MyClass("测试")
    print(f"处理结果: {obj.process()}")
    
    result = example_toolkit.helper_function("hello")
    print(f"辅助函数: {result}")
    
    # 使用子包
    from example_toolkit.subpackage import sub_function
    print(f"子包函数: {sub_function()}")
    
    # 清理
    print("\n=== 清理 ===")
    shutil.rmtree("example_toolkit")
    shutil.rmtree("tests")
    Path("pyproject.toml").unlink()
    Path("README.md").unlink()
    
    print("示例包已删除")
