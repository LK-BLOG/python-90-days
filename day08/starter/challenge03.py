# Day 8 挑战三：CSV 数据处理 (★★★☆☆)
# 要求: 读取、转换、验证、导出 CSV 文件。


import csv
import io
import os


class CSVProcessor:
    """CSV 数据处理器。"""
    
    def __init__(self):
        self._data = []     # 字典列表
        self._headers = []  # 列名
    
    def read(self, filepath, encoding="utf-8", delimiter=","):
        """读取 CSV 文件。"""
        # TODO: 使用 csv.DictReader 读取
        # TODO: 存储 headers 和 data
        pass
    
    def read_string(self, csv_text, delimiter=","):
        """从字符串读取 CSV。"""
        # TODO: 使用 io.StringIO + csv.DictReader
        pass
    
    def validate(self, rules):
        """验证数据。
        
        rules 格式:
            {"age": {"type": int, "min": 0, "max": 150},
             "name": {"type": str, "required": True}}
        
        Returns:
            list: 错误列表 [{"row": n, "field": f, "error": msg}]
        """
        # TODO: 逐行逐字段验证
        pass
    
    def transform(self, column, func):
        """对指定列应用转换函数。"""
        # TODO: 遍历所有行，对指定列调用 func
        pass
    
    def add_column(self, name, func_or_value):
        """添加新列。"""
        # func_or_value: 可以是函数(接收行dict)或固定值
        pass
    
    def filter_rows(self, predicate):
        """按条件过滤行。"""
        pass
    
    def sort_by(self, key, reverse=False):
        """排序。"""
        pass
    
    def to_csv(self, filepath, encoding="utf-8"):
        """导出为 CSV 文件。"""
        # TODO: 使用 csv.DictWriter 写入
        pass
    
    def to_string(self):
        """导出为 CSV 字符串。"""
        pass
    
    def summary(self):
        """返回数据摘要（行数、列数、列名）。"""
        pass


# ===== 测试 =====
if __name__ == "__main__":
    csv_text = """name,age,salary
Alice,25,8000
Bob,30,12000
Charlie,28,9500"""
    
    proc = CSVProcessor()
    proc.read_string(csv_text)
    print(f"摘要: {proc.summary()}")
    print(f"数据: {proc._data}")
    
    proc.add_column("bonus", lambda row: int(row["salary"]) * 10 // 100)
    print(f"加bonus后: {proc._data}")
    
    errors = proc.validate({"age": {"type": int, "min": 0, "max": 150}})
    print(f"验证错误: {errors}")
