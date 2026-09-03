# Day 4 Boss 挑战：日志解析器 (★★★★★)
# 难度: ★★★★★
# 要求: 构建完整的日志解析和分析系统。


import re
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict


class LogEntry:
    """单条日志条目 —— 表示解析后的一条日志记录。
    
    属性:
        timestamp (datetime): 日志时间
        level (str): 日志级别 (INFO/WARNING/ERROR/DEBUG)
        module (str): 来源模块
        message (str): 日志消息
        extra (dict): 额外提取的字段
    """
    
    # 支持的日志格式正则
    LOG_PATTERN = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+'
        r'\[(?P<level>\w+)\]\s+'
        r'(?P<module>\S+)\s*[-:]\s*'
        r'(?P<message>.+)'
    )
    
    def __init__(self, timestamp, level, module, message):
        """初始化日志条目。"""
        self.timestamp = timestamp
        self.level = level.upper()
        self.module = module
        self.message = message
        self.extra = {}
    
    @classmethod
    def from_string(cls, line):
        """从日志字符串解析出 LogEntry。
        
        Args:
            line: 单行日志文本
        
        Returns:
            LogEntry 或 None（解析失败时）
        """
        # TODO: 使用正则匹配日志行
        # TODO: 解析时间戳
        # TODO: 返回 LogEntry 实例
        pass
    
    def matches(self, **filters):
        """检查此条目是否匹配给定的过滤条件。
        
        Args:
            **filters: 可选过滤条件 (level, module, message_pattern)
        
        Returns:
            bool: 是否匹配
        """
        # TODO: 实现多条件过滤
        pass
    
    def __repr__(self):
        return f"LogEntry({self.timestamp}, {self.level}, {self.module})"


class LogAnalyzer:
    """日志分析器 —— 解析、搜索、统计日志文件。
    
    用法:
        >>> analyzer = LogAnalyzer("app.log")
        >>> analyzer.load()
        >>> print(analyzer.get_statistics())
    """
    
    # ANSI 颜色码（终端彩色输出）
    COLORS = {
        "DEBUG": "\033[36m",     # 青色
        "INFO": "\033[32m",      # 绿色
        "WARNING": "\033[33m",   # 黄色
        "ERROR": "\033[31m",     # 红色
        "RESET": "\033[0m",
    }
    
    def __init__(self, filepath, encoding="utf-8"):
        """初始化日志分析器。
        
        Args:
            filepath: 日志文件路径
            encoding: 文件编码
        """
        self.filepath = filepath
        self.encoding = encoding
        self.entries = []        # 解析后的日志条目列表
        self._raw_lines = []     # 原始行
    
    def load(self):
        """加载并解析日志文件。
        
        功能说明:
            逐行读取日志文件，解析每行到 LogEntry 对象。
            解析失败的行保留为 raw_line。
        
        Raises:
            FileNotFoundError: 文件不存在
            PermissionError: 无读取权限
        """
        # TODO: 使用 with 语句读取文件
        # TODO: 逐行调用 LogEntry.from_string
        # TODO: 收集解析成功和失败的行数
        pass
    
    def search(self, keyword=None, level=None, module=None,
               start_time=None, end_time=None):
        """搜索日志条目。
        
        Args:
            keyword: 消息关键词（模糊匹配）
            level: 日志级别
            module: 来源模块
            start_time: 起始时间
            end_time: 结束时间
        
        Returns:
            list: 匹配的 LogEntry 列表
        """
        # TODO: 组合多条件过滤
        pass
    
    def get_statistics(self):
        """生成日志统计信息。
        
        Returns:
            dict: 统计信息 {
                "total": 总条目数,
                "by_level": {级别: 数量},
                "by_module": {模块: 数量},
                "time_range": (最早时间, 最晚时间),
                "errors": [最近的错误条目]
            }
        """
        # TODO: 统计各级别数量
        # TODO: 统计各模块数量
        # TODO: 找出时间范围
        # TODO: 收集最近的错误
        pass
    
    def generate_report(self, output_format="text"):
        """生成日志分析报告。
        
        Args:
            output_format: 输出格式 ("text"/"markdown")
        
        Returns:
            str: 格式化的报告
        """
        # TODO: 调用 get_statistics 获取数据
        # TODO: 根据格式生成报告
        pass
    
    def print_colored(self, entries=None):
        """彩色打印日志条目。
        
        Args:
            entries: 要打印的条目列表，默认全部
        """
        # TODO: 根据日志级别应用 ANSI 颜色
        pass


# ===== 测试 =====
if __name__ == "__main__":
    # 创建示例日志文件进行测试
    sample_log = """2024-01-15 10:30:00 [INFO] app.main: 应用启动
2024-01-15 10:30:01 [DEBUG] app.db: 数据库连接成功
2024-01-15 10:30:05 [WARNING] app.cache: 缓存命中率低: 45%
2024-01-15 10:30:10 [ERROR] app.api: 请求超时: /api/users
2024-01-15 10:30:15 [INFO] app.main: 处理请求 /api/data
2024-01-15 10:30:20 [ERROR] app.db: 连接池耗尽
2024-01-15 10:30:25 [INFO] app.main: 请求完成
"""
    
    test_file = "_test_sample.log"
    try:
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(sample_log)
        
        analyzer = LogAnalyzer(test_file)
        analyzer.load()
        
        print(f"解析条目数: {len(analyzer.entries)}")
        print(f"\n统计信息:")
        stats = analyzer.get_statistics()
        for k, v in stats.items():
            print(f"  {k}: {v}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
