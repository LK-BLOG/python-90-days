"""
Challenge 02: 日志系统 - LogCraft
"""
import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, TextIO
from pathlib import Path
from collections import deque
import threading


class LogLevel:
    """日志级别"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class LogFormatter:
    """日志格式化器"""
    
    def __init__(self, format_str: str = None, json_format: bool = False):
        self.format_str = format_str
        self.json_format = json_format
    
    def format(self, level: int, message: str, **kwargs) -> str:
        """格式化日志消息
        
        TODO: 实现格式化
        - 支持普通文本格式
        - 支持 JSON 格式
        """
        pass


class LogHandler:
    """日志处理器基类"""
    
    def __init__(self, level: int = LogLevel.DEBUG, formatter: LogFormatter = None):
        self.level = level
        self.formatter = formatter or LogFormatter()
    
    def emit(self, level: int, message: str, **kwargs):
        """发送日志"""
        if level >= self.level:
            formatted = self.formatter.format(level, message, **kwargs)
            self.write(formatted)
    
    def write(self, message: str):
        """写入日志（子类实现）"""
        raise NotImplementedError


class ConsoleHandler(LogHandler):
    """控制台处理器"""
    
    def write(self, message: str):
        """写入控制台"""
        # TODO: 实现
        pass


class FileHandler(LogHandler):
    """文件处理器"""
    
    def __init__(self, filename: str, level: int = LogLevel.DEBUG, 
                 formatter: LogFormatter = None, max_bytes: int = 10*1024*1024,
                 backup_count: int = 5):
        super().__init__(level, formatter)
        self.filename = filename
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.current_size = 0
    
    def write(self, message: str):
        """写入文件
        
        TODO: 实现
        - 写入文件
        - 检查文件大小
        - 实现日志轮转
        """
        pass
    
    def rotate(self):
        """日志轮转
        
        TODO: 实现日志轮转
        - 重命名旧文件
        - 创建新文件
        """
        pass


class Logger:
    """日志器"""
    
    def __init__(self, name: str, level: int = LogLevel.DEBUG):
        self.name = name
        self.level = level
        self.handlers: List[LogHandler] = []
        self._lock = threading.Lock()
    
    def add_handler(self, handler: LogHandler):
        """添加处理器"""
        self.handlers.append(handler)
    
    def remove_handler(self, handler: LogHandler):
        """移除处理器"""
        self.handlers.remove(handler)
    
    def log(self, level: int, message: str, **kwargs):
        """记录日志"""
        if level >= self.level:
            with self._lock:
                for handler in self.handlers:
                    handler.emit(level, message, logger_name=self.name, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """调试日志"""
        self.log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """信息日志"""
        self.log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告日志"""
        self.log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """错误日志"""
        self.log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """严重错误日志"""
        self.log(LogLevel.CRITICAL, message, **kwargs)


def create_logger(
    name: str,
    level: int = LogLevel.INFO,
    console: bool = True,
    file: str = None,
    json_format: bool = False
) -> Logger:
    """创建日志器的便捷函数
    
    TODO: 实现
    - 创建 Logger
    - 添加 ConsoleHandler
    - 添加 FileHandler（如果指定）
    """
    pass


if __name__ == "__main__":
    logger = create_logger("test", level=LogLevel.DEBUG, console=True)
    logger.info("日志系统启动")
    logger.debug("调试信息")
    logger.warning("警告信息")
    logger.error("错误信息")
