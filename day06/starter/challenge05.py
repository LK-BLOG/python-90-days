# Day 6 挑战五 (Boss)：数据加载器 (★★★★★)
# 要求: 构建带完整异常处理的数据加载系统。


import json
import csv
import io
from pathlib import Path


class DataLoadError(Exception):
    """数据加载异常基类。"""
    pass


class FileFormatError(DataLoadError):
    """文件格式错误。"""
    pass


class DataValidationError(DataLoadError):
    """数据验证错误。"""
    pass


class DataLoader:
    """通用数据加载器 —— 支持 JSON/CSV/纯文本，带验证和重试。
    
    用法:
        loader = DataLoader()
        data = loader.load("users.json")
    """
    
    SUPPORTED_FORMATS = {".json", ".csv", ".txt", ".tsv"}
    
    def __init__(self, encoding="utf-8", strict=True, max_retries=2):
        self.encoding = encoding
        self.strict = strict
        self.max_retries = max_retries
        self._errors = []
    
    def load(self, filepath, schema=None):
        """加载数据文件。
        
        Args:
            filepath: 文件路径
            schema: 可选的验证 schema
        
        Returns:
            加载后的数据
        """
        # TODO: 检查文件格式
        # TODO: 根据扩展名分派到对应解析方法
        # TODO: 应用 schema 验证
        # TODO: 失败时重试
        pass
    
    def _load_json(self, filepath):
        """加载 JSON 文件。"""
        # TODO: 读取并解析，处理 JSONDecodeError
        pass
    
    def _load_csv(self, filepath):
        """加载 CSV 文件。"""
        # TODO: 用 csv.DictReader 读取
        pass
    
    def _load_text(self, filepath):
        """加载纯文本文件（按行返回）。"""
        pass
    
    def _validate(self, data, schema):
        """验证数据是否符合 schema。"""
        # TODO: 遍历 schema 检查类型和必填字段
        pass
    
    def get_errors(self):
        """返回加载过程中的所有错误。"""
        return list(self._errors)
    
    def load_string(self, content, format="json", schema=None):
        """从字符串加载数据（不依赖文件）。"""
        # TODO: 解析字符串内容
        pass


# ===== 测试 =====
if __name__ == "__main__":
    # JSON 测试
    json_content = '{"users": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]}'
    loader = DataLoader()
    data = loader.load_string(json_content, format="json")
    print(f"JSON 加载: {data}")
    
    # CSV 测试
    csv_content = "name,age\nAlice,25\nBob,30\nCharlie,28"
    data = loader.load_string(csv_content, format="csv")
    print(f"CSV 加载: {data}")
    
    # 错误处理测试
    try:
        loader.load_string("{bad json}", format="json")
    except FileFormatError as e:
        print(f"格式错误: {e}")
