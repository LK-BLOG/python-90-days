# Day 27 - Boss Challenge: 多 API 聚合系统
# 难度: ⭐⭐⭐⭐⭐
# GitHub + 天气 + 新闻等多 API 聚合，数据清洗转换，生成 Markdown 报告

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class DataSource:
    """数据源配置"""
    name: str
    api_url: str
    api_key: str = ""
    fetcher: Callable = None
    transformer: Callable[[dict], dict] = None
    priority: int = 0  # 越大优先级越高


@dataclass
class CleanedData:
    """清洗后的数据"""
    source: str
    timestamp: str
    data: dict
    quality_score: float  # 0-1 数据质量评分


class MultiAPISystem:
    """多 API 聚合系统

    从多个 API 并发获取数据，清洗转换，智能合并，生成报告。
    """

    def __init__(self, report_dir: str = "reports"):
        """初始化

        Args:
            report_dir: 报告输出目录
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        # TODO: 注册数据源
        self._sources: list[DataSource] = []
        # TODO: 定时更新配置
        self._schedule_interval: int = 3600  # 秒

    def register_source(self, source: DataSource) -> None:
        """注册数据源"""
        # TODO: 按优先级插入
        ...

    def fetch_all(self) -> dict[str, Any]:
        """并发获取所有数据源"""
        # TODO: ThreadPoolExecutor 并发请求
        ...

    def clean_and_transform(self, raw_data: dict[str, Any]) -> list[CleanedData]:
        """清洗和转换原始数据

        Args:
            raw_data: {数据源名: 原始数据}

        Returns:
            清洗后的数据列表
        """
        # TODO: 去除空值和无效数据
        # TODO: 标准化字段名
        # TODO: 添加时间戳和质量评分
        ...

    def smart_merge(self, cleaned: list[CleanedData]) -> dict:
        """智能合并多个数据源

        Args:
            cleaned: 清洗后的数据列表

        Returns:
            合并后的数据
        """
        # TODO: 按优先级合并
        # TODO: 同名字段取高优先级值
        # TODO: 列表字段合并去重
        ...

    def generate_markdown_report(self, merged: dict) -> str:
        """生成 Markdown 报告

        Args:
            merged: 合并后的数据

        Returns:
            Markdown 报告
        """
        # TODO: 生成包含以下内容的报告：
        # - 报告标题和生成时间
        # - 数据源状态汇总
        # - 各数据源详情
        # - 合并后的完整数据
        # - 质量评分统计
        ...

    def save_report(self, content: str, filename: str = None) -> Path:
        """保存报告到文件

        Args:
            content: 报告内容
            filename: 文件名，None 则自动生成

        Returns:
            报告文件路径
        """
        # TODO: 生成带时间戳的文件名
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    system = MultiAPISystem()
    print("多 API 聚合系统初始化完成")
    print("请通过 register_source() 注册数据源后调用 fetch_all()")
