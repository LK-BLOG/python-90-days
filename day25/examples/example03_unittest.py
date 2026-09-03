"""示例3：unittest 完整示例"""
import unittest
import tempfile
import os
from pathlib import Path


class Calculator:
    """简单的计算器类"""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def get_history(self):
        return self.history.copy()


class TestCalculator(unittest.TestCase):
    """计算器测试"""
    
    def setUp(self):
        """每个测试方法前执行"""
        self.calc = Calculator()
    
    def test_add(self):
        """测试加法"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)
    
    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5.0)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.333333, places=5)
    
    def test_divide_by_zero(self):
        """测试除以零"""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertEqual(str(context.exception), "除数不能为零")
    
    def test_history(self):
        """测试历史记录"""
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("1 + 2 = 3", history)
        self.assertIn("5 - 3 = 2", history)
    
    def test_history_is_copy(self):
        """测试历史记录是副本"""
        self.calc.add(1, 2)
        history = self.calc.get_history()
        history.append("tampered")
        
        # 原始历史不应被修改
        self.assertEqual(len(self.calc.get_history()), 1)


class TestFileManager(unittest.TestCase):
    """文件管理器测试（展示 setUp/tearDown）"""
    
    @classmethod
    def setUpClass(cls):
        """整个测试类只执行一次"""
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """整个测试类结束后执行"""
        import shutil
        shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        """每个测试方法前执行"""
        self.file_path = os.path.join(self.temp_dir, f"test_{id(self)}.txt")
    
    def tearDown(self):
        """每个测试方法后执行"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
    
    def test_write_and_read(self):
        """测试写入和读取"""
        content = "Hello, World!"
        
        with open(self.file_path, "w") as f:
            f.write(content)
        
        with open(self.file_path) as f:
            read_content = f.read()
        
        self.assertEqual(read_content, content)
    
    def test_file_not_exists(self):
        """测试文件不存在"""
        self.assertFalse(os.path.exists(self.file_path))


class TestMockExample(unittest.TestCase):
    """Mock 示例"""
    
    def test_mock_basic(self):
        """基础 Mock"""
        from unittest.mock import Mock
        
        mock_obj = Mock()
        mock_obj.method.return_value = 42
        
        result = mock_obj.method()
        
        self.assertEqual(result, 42)
        mock_obj.method.assert_called_once()
    
    def test_mock_call_args(self):
        """检查调用参数"""
        from unittest.mock import Mock
        
        mock_func = Mock()
        mock_func("arg1", key="value")
        
        mock_func.assert_called_once_with("arg1", key="value")
    
    def test_patch_example(self):
        """patch 示例"""
        from unittest.mock import patch
        
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            
            result = os.path.exists("/some/path")
            
            self.assertTrue(result)
            mock_exists.assert_called_once_with("/some/path")


if __name__ == "__main__":
    unittest.main()
