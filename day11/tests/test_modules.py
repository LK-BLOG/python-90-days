# test_modules.py - 模块系统测试用例
import unittest
import tempfile
import os
import sys
from pathlib import Path

class TestModules(unittest.TestCase):
    """测试模块系统"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_path = sys.path.copy()
    
    def tearDown(self):
        """测试后清理"""
        # 恢复sys.path
        sys.path = self.original_path
        
        # 删除临时目录
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_module_creation(self):
        """测试模块创建"""
        # 创建测试模块
        module_content = '''
def hello():
    return "Hello from module!"
'''
        module_file = self.test_dir / "test_module.py"
        module_file.write_text(module_content, encoding='utf-8')
        
        # 添加到sys.path
        sys.path.insert(0, str(self.test_dir))
        
        # 导入模块
        import test_module
        result = test_module.hello()
        
        self.assertEqual(result, "Hello from module!")
    
    def test_package_creation(self):
        """测试包创建"""
        # 创建包目录
        package_dir = self.test_dir / "test_package"
        package_dir.mkdir()
        
        # 创建__init__.py
        init_content = '''
from .module import hello
'''
        (package_dir / "__init__.py").write_text(init_content, encoding='utf-8')
        
        # 创建模块
        module_content = '''
def hello():
    return "Hello from package!"
'''
        (package_dir / "module.py").write_text(module_content, encoding='utf-8')
        
        # 添加到sys.path
        sys.path.insert(0, str(self.test_dir))
        
        # 导入包
        from test_package import hello
        result = hello()
        
        self.assertEqual(result, "Hello from package!")

if __name__ == "__main__":
    unittest.main(verbosity=2)
