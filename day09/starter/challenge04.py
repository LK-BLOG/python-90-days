# Day 9 挑战四：数据转换工具 (★★★★☆)
# 要求: 在不同数据格式间转换。


import json
import csv
import io


class DataConverter:
    """数据格式转换器。"""
    
    @staticmethod
    def json_to_csv(json_str, output_path=None):
        """JSON 字符串 -> CSV。"""
        # TODO: 解析 JSON，提取列名，生成 CSV
        pass
    
    @staticmethod
    def csv_to_json(csv_str, orient="records"):
        """CSV 字符串 -> JSON。
        
        orient: "records" -> [{"a":1}, ...]
                "columns" -> {"col1": [...], "col2": [...]}
                "index"   -> {"0": {"a":1}, ...}
        """
        # TODO: 解析 CSV 并按 orient 格式输出
        pass
    
    @staticmethod
    def flatten_json(nested, prefix=""):
        """嵌套 JSON -> 扁平化键值对。"""
        # TODO: 递归展平 {"a": {"b": 1}} -> {"a.b": 1}
        pass
    
    @staticmethod
    def unflatten_json(flat):
        """扁平化键值对 -> 嵌套 JSON。"""
        # TODO: 反向操作
        pass
    
    @staticmethod
    def transform(data, mapping):
        """按 mapping 规则转换数据结构。
        
        mapping: {"new_key": "old.path", "computed": lambda row: ...}
        """
        pass


# ===== 测试 =====
if __name__ == "__main__":
    json_data = '[{"name":"Alice","age":25},{"name":"Bob","age":30}]'
    
    csv_out = DataConverter.json_to_csv(json_data)
    print(f"JSON->CSV:\n{csv_out}")
    
    flat = DataConverter.flatten_json({"a": {"b": {"c": 1}}, "d": 2})
    print(f"展平: {flat}")
    
    nested = DataConverter.unflatten_json({"a.b.c": 1, "d": 2})
    print(f"反展平: {nested}")
