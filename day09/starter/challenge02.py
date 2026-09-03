# Day 9 挑战二：JSON 数据验证器 (★★★☆☆)
# 要求: 根据 schema 验证 JSON 数据。


import json
from typing import Any, Dict, List, Optional


class JSONValidator:
    """JSON 数据验证器 —— 根据 schema 验证数据结构。
    
    schema 示例:
        {
            "name": {"type": str, "required": True, "min_length": 1},
            "age": {"type": int, "min": 0, "max": 150},
            "tags": {"type": list, "items": {"type": str}},
            "address": {
                "type": dict,
                "schema": {
                    "city": {"type": str, "required": True}
                }
            }
        }
    """
    
    def __init__(self, schema):
        self.schema = schema
        self._errors = []
    
    def validate(self, data):
        """验证数据。
        
        Returns:
            tuple: (is_valid: bool, errors: list of str)
        """
        self._errors = []
        self._validate_dict(data, self.schema, "")
        return (len(self._errors) == 0, list(self._errors))
    
    def _validate_dict(self, data, schema, path):
        """递归验证字典。"""
        # TODO: 检查必填字段
        # TODO: 遍历 schema 验证每个字段
        pass
    
    def _validate_field(self, value, rules, path):
        """验证单个字段。"""
        # TODO: 类型检查
        # TODO: min/max 范围
        # TODO: min_length/max_length
        # TODO: choices 约束
        pass
    
    def _validate_list(self, data, rules, path):
        """验证列表字段。"""
        # TODO: 检查是否为 list
        # TODO: 验证 items 规则
        pass
    
    def validate_file(self, filepath):
        """从文件加载并验证。"""
        # TODO: 读取 JSON 文件并验证
        pass
    
    def validate_string(self, json_str):
        """从 JSON 字符串验证。"""
        pass


class SchemaBuilder:
    """Schema 构建器 —— 链式 API 构建验证规则。"""
    
    def __init__(self, field_name):
        self._rules = {"name": field_name}
    
    def type(self, t):
        self._rules["type"] = t
        return self
    
    def required(self, r=True):
        self._rules["required"] = r
        return self
    
    def range(self, min_val=None, max_val=None):
        if min_val is not None: self._rules["min"] = min_val
        if max_val is not None: self._rules["max"] = max_val
        return self
    
    def length(self, min_len=None, max_len=None):
        if min_len is not None: self._rules["min_length"] = min_len
        if max_len is not None: self._rules["max_length"] = max_len
        return self
    
    def choices(self, options):
        self._rules["choices"] = options
        return self
    
    def build(self):
        return self._rules


# ===== 测试 =====
if __name__ == "__main__":
    schema = {
        "name": {"type": str, "required": True, "min_length": 1},
        "age": {"type": int, "min": 0, "max": 150},
        "email": {"type": str},
        "tags": {"type": list, "items": {"type": str}},
    }
    
    validator = JSONValidator(schema)
    
    ok, errors = validator.validate({"name": "Alice", "age": 25, "tags": ["a", "b"]})
    print(f"有效数据: ok={ok}, errors={errors}")
    
    ok, errors = validator.validate({"name": "", "age": -5})
    print(f"无效数据: ok={ok}, errors={errors}")
