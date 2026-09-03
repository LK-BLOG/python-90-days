"""Day 30 - 日志工具"""
from __future__ import annotations

import logging
import sys


def setup_logger(name: str = "ai_assistant", level: str = "INFO",
                 log_file: str = None) -> logging.Logger:
    """配置日志系统

    Args:
        name: 日志器名称
        level: 日志级别
        log_file: 日志文件路径

    Returns:
        配置好的 Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # 控制台输出
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(handler)

    # 文件输出
    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))
        logger.addHandler(fh)

    return logger
