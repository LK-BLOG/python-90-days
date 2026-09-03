# test_package.py - 包测试用例
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

class TestPackage(unittest.TestCase):
    """测试包结构"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_path = sys.path.copy()
    
    def tearDown(self):
        """测试后清理"""
        sys.path = self.original_path
        shutil.rmtree(self.test_dir)
    
    def test_package_structure(self):
        """测试包结构"""
        # 创建包
        package_dir = self.test_dir / "test_package"
        package_dir.mkdir()
        
        # 创建__init__.py
        init_content = '''
def hello():
    return "Hello from package!"
'''
        (package_dir / "__init__.py").write_text(init_content, encoding='utf-8')
        
        # 添加到sys.path
        sys.path.insert(0, str(self.test_dir))
        
        # 导入包
        import test_package
        result = test_package.hello()
        
        self.assertEqual(result, "Hello from package!")

if __name__ == "__main__":
    unittest.main(verbosity=2)
