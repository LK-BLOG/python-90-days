# Day 9 挑战五 (Boss)：通用数据迁移工具 (★★★★★)
# 要求: 在不同数据源和格式间迁移数据。


import json
import csv
import os
from pathlib import Path
from datetime import datetime


class DataMigration:
    """数据迁移工具 —— 从源读取、转换、写入目标。"""
    
    def __init__(self, name="migration"):
        self.name = name
        self._steps = []
        self._log = []
    
    def source(self, reader_func, **kwargs):
        """设置数据源。"""
        # TODO: 存储 reader 函数和参数
        pass
    
    def transform(self, transform_func, name="step"):
        """添加转换步骤。"""
        pass
    
    def destination(self, writer_func, **kwargs):
        """设置输出目标。"""
        pass
    
    def run(self):
        """执行迁移管道。"""
        # TODO: 读取 -> 逐个转换 -> 写入
        pass
    
    def get_log(self):
        return list(self._log)


# 预定义读写器
def read_json_file(filepath, encoding="utf-8"):
    """JSON 文件读取器。"""
    pass

def read_csv_file(filepath, encoding="utf-8"):
    """CSV 文件读取器。"""
    pass

def write_json_file(filepath, encoding="utf-8"):
    """JSON 文件写入器（返回写入函数）。"""
    pass

def write_csv_file(filepath, encoding="utf-8"):
    """CSV 文件写入器（返回写入函数）。"""
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("请实现 DataMigration 后运行测试")
