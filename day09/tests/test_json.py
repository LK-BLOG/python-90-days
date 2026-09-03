# test_json.py - JSON测试用例
import unittest
import json
import tempfile
import os

class TestJSONOperations(unittest.TestCase):
    """测试JSON操作"""
    
    def test_basic_serialization(self):
        """测试基础序列化"""
        data = {"name": "test", "value": 123}
        json_str = json.dumps(data)
        self.assertEqual(json_str, '{"name": "test", "value": 123}')
    
    def test_basic_deserialization(self):
        """测试基础反序列化"""
        json_str = '{"name": "test", "value": 123}'
        data = json.loads(json_str)
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["value"], 123)
    
    def test_file_operations(self):
        """测试文件操作"""
        data = {"test": "data"}
        filename = tempfile.mktemp(suffix='.json')
        
        try:
            # 写入
            with open(filename, 'w') as f:
                json.dump(data, f)
            
            # 读取
            with open(filename, 'r') as f:
                loaded = json.load(f)
            
            self.assertEqual(loaded, data)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

if __name__ == "__main__":
    unittest.main(verbosity=2)
