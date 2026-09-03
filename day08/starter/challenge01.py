# Day 8 挑战一：日志文件分析器 (★★★☆☆)
# 要求: 读取和分析日志文件。


import re
import os
from collections import Counter, defaultdict
from datetime import datetime


class LogAnalyzer:
    """日志分析工具。
    
    用法:
        analyzer = LogAnalyzer("app.log")
        analyzer.analyze()
        stats = analyzer.get_statistics()
    """
    
    # 支持的日志格式: 2024-01-15 10:30:00 [INFO] message
    LOG_PATTERN = re.compile(
        r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+'
        r'\[(\w+)\]\s+(.+)'
    )
    
    def __init__(self, filepath, encoding="utf-8"):
        self.filepath = filepath
        self.encoding = encoding
        self.entries = []        # 解析后的条目
        self._stats = {}         # 统计结果
        self._search_index = {}  # 关键词索引
    
    def analyze(self):
        """读取并解析日志文件。"""
        # TODO: 用 with + encoding 读取文件
        # TODO: 逐行用正则解析
        # TODO: 存入 self.entries
        pass
    
    def get_statistics(self):
        """返回统计信息。"""
        # TODO: 统计各 level 数量
        # TODO: 统计时间范围
        # TODO: 统计每小时分布
        pass
    
    def search(self, keyword, level=None):
        """搜索日志。"""
        # TODO: 关键词匹配 + 可选级别过滤
        pass
    
    def tail(self, n=10):
        """获取最后 n 条日志。"""
        return self.entries[-n:]
    
    def time_distribution(self):
        """按小时统计日志分布。"""
        # TODO: 返回 {hour: count} 字典
        pass


# ===== 测试 =====
if __name__ == "__main__":
    sample = """2024-01-15 10:00:00 [INFO] 应用启动
2024-01-15 10:01:00 [DEBUG] 加载配置
2024-01-15 10:02:00 [WARNING] 缓存命中率低
2024-01-15 10:03:00 [ERROR] 连接超时
2024-01-15 10:05:00 [INFO] 请求处理完成"""
    test_file = "_test.log"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(sample)
    
    analyzer = LogAnalyzer(test_file)
    analyzer.analyze()
    print(f"条目数: {len(analyzer.entries)}")
    print(f"统计: {analyzer.get_statistics()}")
    print(f"尾部: {[str(e) for e in analyzer.tail(2)]}")
    os.remove(test_file)
