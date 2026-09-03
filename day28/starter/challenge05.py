# Day 28 - Challenge 5: 异步爬虫框架
# 难度: ⭐⭐⭐⭐
# URL 队列管理、并发控制、重试机制、数据存储

import asyncio
import time
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


@dataclass
class CrawlTask:
    """爬取任务"""
    url: str
    depth: int = 0
    priority: int = 0
    retries: int = 0
    max_retries: int = 3
    callback: Optional[Callable] = None


@dataclass
class CrawlResult:
    """爬取结果"""
    url: str
    status_code: int = 0
    body: str = ""
    links: list[str] = field(default_factory=list)
    elapsed_ms: float = 0.0
    error: str | None = None
    depth: int = 0


class AsyncCrawler:
    """异步爬虫框架

    支持 URL 队列管理、并发控制、重试、数据存储。
    """

    def __init__(self, max_concurrent: int = 10, max_depth: int = 3,
                 storage_path: str = "crawl_data.json"):
        """初始化

        Args:
            max_concurrent: 最大并发数
            max_depth: 最大爬取深度
            storage_path: 数据存储路径
        """
        self.max_concurrent = max_concurrent
        self.max_depth = max_depth
        self.storage_path = Path(storage_path)
        # TODO: 初始化队列、并发控制、已访问集合
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._visited: set[str] = set()
        self._results: list[CrawlResult] = []
        self._queue: asyncio.Queue = None

    async def start(self, seed_urls: list[str]) -> list[CrawlResult]:
        """从种子 URL 开始爬取

        Args:
            seed_urls: 起始 URL 列表

        Returns:
            所有爬取结果
        """
        # TODO: 将种子 URL 入队
        # TODO: 创建 worker 协程并发处理
        # TODO: 等待队列清空
        ...

    async def _worker(self, worker_id: int) -> None:
        """Worker 协程，持续从队列取任务处理

        Args:
            worker_id: Worker 编号
        """
        # TODO: 循环从队列获取任务
        # TODO: 检查是否已访问
        # TODO: 发送请求、解析、提取链接、重试
        ...

    async def _fetch_one(self, task: CrawlTask) -> CrawlResult:
        """执行单个爬取任务

        Args:
            task: 爬取任务

        Returns:
            爬取结果
        """
        # TODO: 使用 semaphore 限制并发
        # TODO: 发送 HTTP 请求
        # TODO: 解析响应，提取链接
        # TODO: 失败时重试（指数退避）
        ...

    def _extract_links(self, html: str, base_url: str) -> list[str]:
        """从 HTML 中提取链接

        Args:
            html: HTML 内容
            base_url: 基础 URL

        Returns:
            提取到的链接列表
        """
        # TODO: 简单的正则或字符串匹配提取 <a href="...">
        ...

    def save_results(self) -> None:
        """保存爬取结果到文件"""
        # TODO: 将 _results 序列化为 JSON
        ...

    def get_stats(self) -> dict:
        """获取爬取统计"""
        return {
            "visited": len(self._visited),
            "results": len(self._results),
            "errors": sum(1 for r in self._results if r.error),
        }


# ==================== 测试 ====================
if __name__ == "__main__":
    async def main():
        crawler = AsyncCrawler(max_concurrent=5, max_depth=2)
        # results = await crawler.start(["https://example.com"])
        # print(f"爬取完成: {crawler.get_stats()}")
        print("异步爬虫框架初始化完成")
        print("取消注释 start() 调用以实际爬取")

    asyncio.run(main())
