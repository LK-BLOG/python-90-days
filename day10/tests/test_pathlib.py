# test_pathlib.py - pathlib测试用例
import unittest
import tempfile
import shutil
from pathlib import Path

class TestPathlibOperations(unittest.TestCase):
    """测试pathlib操作"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_path_creation(self):
        """测试路径创建"""
        file_path = self.test_dir / "test.txt"
        self.assertEqual(file_path.name, "test.txt")
        self.assertEqual(file_path.parent, self.test_dir)
    
    def test_file_operations(self):
        """测试文件操作"""
        # 创建文件
        file_path = self.test_dir / "test.txt"
        file_path.write_text("测试内容", encoding='utf-8')
        
        # 检查文件
        self.assertTrue(file_path.exists())
        self.assertTrue(file_path.is_file())
        
        # 读取文件
        content = file_path.read_text(encoding='utf-8')
        self.assertEqual(content, "测试内容")
    
    def test_directory_operations(self):
        """测试目录操作"""
        # 创建目录
        dir_path = self.test_dir / "subdir"
        dir_path.mkdir()
        
        # 检查目录
        self.assertTrue(dir_path.exists())
        self.assertTrue(dir_path.is_dir())
    
    def test_glob_pattern(self):
        """测试glob模式匹配"""
        # 创建测试文件
        for i in range(3):
            (self.test_dir / f"test_{i}.txt").write_text(f"内容 {i}")
        
        # 匹配文件
        txt_files = list(self.test_dir.glob("*.txt"))
        self.assertEqual(len(txt_files), 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
