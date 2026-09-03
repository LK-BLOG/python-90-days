# Day 25 - Challenge 2: 日志系统
# 难度: ⭐⭐⭐
# 多输出目标、日志轮转、结构化日志、性能友好的过滤

import json
import logging
import logging.handlers
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class StructuredFormatter(logging.Formatter):
    """结构化 JSON 日志格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        """将日志记录格式化为 JSON 字符串

        Args:
            record: 日志记录

        Returns:
            JSON 格式的日志字符串
        """
        # TODO: 构建包含 timestamp, level, logger, message, extra 等字段的字典
        # TODO: 序列化为 JSON
        ...


class PerformanceFilter(logging.Filter):
    """性能友好的日志过滤器

    支持按级别、模块名、消息模式过滤，减少不必要的日志开销。
    """

    def __init__(self, min_level: int = logging.DEBUG,
                 include_patterns: list[str] = None,
                 exclude_patterns: list[str] = None):
        """初始化过滤器

        Args:
            min_level: 最低日志级别
            include_patterns: 只包含匹配的消息模式
            exclude_patterns: 排除匹配的消息模式
        """
        super().__init__()
        self.min_level = min_level
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []

    def filter(self, record: logging.LogRecord) -> bool:
        """判断是否应该记录该日志

        Args:
            record: 日志记录

        Returns:
            True 表示应该记录
        """
        # TODO: 实现级别检查、包含/排除模式匹配
        ...


class LoggingSystem:
    """可配置的日志系统

    支持多输出目标、日志轮转、结构化日志。
    """

    def __init__(self, name: str = "app", log_dir: str = "logs"):
        """初始化日志系统

        Args:
            name: 日志器名称
            log_dir: 日志文件目录
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # TODO: 创建 logger
        self._logger = logging.getLogger(name)

    def setup_console(self, level: int = logging.INFO,
                      use_json: bool = False) -> None:
        """添加控制台输出

        Args:
            level: 日志级别
            use_json: 是否使用 JSON 格式
        """
        # TODO: 创建 StreamHandler，设置格式，添加到 logger
        ...

    def setup_file(self, filename: str = "app.log",
                   level: int = logging.DEBUG,
                   max_bytes: int = 10 * 1024 * 1024,
                   backup_count: int = 5) -> None:
        """添加文件输出（带轮转）

        Args:
            filename: 日志文件名
            level: 日志级别
            max_bytes: 单文件最大字节数
            backup_count: 保留的备份数量
        """
        # TODO: 创建 RotatingFileHandler
        ...

    def setup_timed_file(self, filename: str = "timed.log",
                         when: str = "midnight",
                         interval: int = 1) -> None:
        """添加按时间轮转的文件输出

        Args:
            filename: 日志文件名
            when: 轮转时机（midnight/hourly 等）
            interval: 轮转间隔
        """
        # TODO: 创建 TimedRotatingFileHandler
        ...

    def get_logger(self) -> logging.Logger:
        """获取配置好的 logger"""
        return self._logger


# ==================== 测试 ====================
if __name__ == "__main__":
    system = LoggingSystem("demo", log_dir="demo_logs")
    system.setup_console(level=logging.DEBUG)
    system.setup_file("demo.log")

    logger = system.get_logger()
    logger.debug("这是一条调试日志")
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    print("日志系统初始化完成")
