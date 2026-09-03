# Day 27 - Challenge 5: API 聚合服务
# 难度: ⭐⭐⭐⭐
# 同时调用多个 API、数据合并、错误处理、结果缓存

import time
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class APIEndpoint:
    """API 端点描述"""
    name: str
    url: str
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)
    timeout: int = 10
    transform: Callable[[dict], dict] | None = None


@dataclass
class AggregatedResult:
    """聚合结果"""
    sources: dict[str, Any] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)
    cache_hits: int = 0
    total_time_ms: float = 0.0


class APIAggregator:
    """API 聚合服务

    同时调用多个 API，合并结果，支持缓存和错误处理。
    """

    def __init__(self, cache_ttl: int = 300, max_workers: int = 5):
        """初始化

        Args:
            cache_ttl: 缓存过期时间（秒）
            max_workers: 最大并发线程数
        """
        self.cache_ttl = cache_ttl
        self.max_workers = max_workers
        # TODO: 初始化端点列表和缓存
        self._endpoints: list[APIEndpoint] = []
        self._cache: dict[str, tuple[float, Any]] = {}
        self._cache_file = Path("api_cache.json")

    def register_endpoint(self, endpoint: APIEndpoint) -> None:
        """注册 API 端点

        Args:
            endpoint: API 端点描述
        """
        # TODO: 添加到端点列表
        ...

    def _fetch_one(self, endpoint: APIEndpoint) -> tuple[str, Any, str]:
        """获取单个 API 的数据

        Args:
            endpoint: API 端点

        Returns:
            (名称, 数据, 错误信息) 三元组
        """
        # TODO: 检查缓存
        # TODO: 发送 HTTP 请求
        # TODO: 应用 transform 函数
        # TODO: 写入缓存
        ...

    def aggregate(self, endpoints: list[APIEndpoint] = None) -> AggregatedResult:
        """并发调用所有 API 并聚合结果

        Args:
            endpoints: 指定端点列表，None 使用已注册的

        Returns:
            AggregatedResult 聚合结果
        """
        # TODO: 使用 ThreadPoolExecutor 并发请求
        # TODO: 收集成功结果和错误
        # TODO: 合并到 AggregatedResult
        ...

    def merge_data(self, results: dict[str, Any]) -> dict:
        """智能合并多个数据源

        Args:
            results: {数据源名: 数据} 映射

        Returns:
            合并后的数据
        """
        # TODO: 合并同名字段，冲突时优先选择非空值
        ...

    def generate_report(self, result: AggregatedResult) -> str:
        """生成 Markdown 聚合报告

        Args:
            result: 聚合结果

        Returns:
            Markdown 报告文本
        """
        # TODO: 生成包含成功/失败统计、耗时、数据摘要的报告
        ...

    def clear_cache(self) -> int:
        """清空缓存

        Returns:
            清除的缓存条目数
        """
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    aggregator = APIAggregator()
    print("API 聚合服务初始化完成")
    print("请通过 register_endpoint() 注册 API 端点后调用 aggregate()")
