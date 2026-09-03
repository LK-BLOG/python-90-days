# Day 28 - Challenge 3: 异步 HTTP 客户端
# 难度: ⭐⭐⭐
# GET/POST、并发请求、限速控制、错误处理

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError


@dataclass
class AsyncResponse:
    """异步 HTTP 响应"""
    url: str
    status_code: int = 0
    body: bytes = b""
    elapsed_ms: float = 0.0
    error: str | None = None


class RateLimiter:
    """异步速率限制器"""

    def __init__(self, rate: float, period: float = 1.0):
        """初始化

        Args:
            rate: 时间窗口内允许的请求数
            period: 时间窗口（秒）
        """
        self.rate = rate
        self.period = period
        # TODO: 实现令牌桶或滑动窗口限速
        self._tokens = rate
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """获取一个令牌，如果需要则等待"""
        # TODO: 检查令牌，不足时 sleep 等待
        ...


class AsyncHTTPClient:
    """异步 HTTP 客户端

    使用 asyncio + ThreadPoolExecutor 实现异步 HTTP 请求。
    """

    def __init__(self, max_concurrent: int = 10, rate_limit: float = 20.0):
        """初始化

        Args:
            max_concurrent: 最大并发连接数
            rate_limit: 每秒最大请求数
        """
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._rate_limiter = RateLimiter(rate_limit)
        # TODO: 初始化统计信息
        self._stats = {"total": 0, "success": 0, "failed": 0}

    async def get(self, url: str, headers: dict = None,
                  timeout: float = 10.0) -> AsyncResponse:
        """异步 GET 请求

        Args:
            url: 请求 URL
            headers: 请求头
            timeout: 超时时间

        Returns:
            AsyncResponse 对象
        """
        # TODO: 获取速率限制令牌
        # TODO: 在线程池中执行同步 HTTP 请求
        ...

    async def post(self, url: str, data: Any = None,
                   headers: dict = None) -> AsyncResponse:
        """异步 POST 请求"""
        ...

    async def fetch_many(self, urls: list[str],
                         progress_callback: Callable = None) -> list[AsyncResponse]:
        """并发请求多个 URL

        Args:
            urls: URL 列表
            progress_callback: 进度回调 (completed, total)

        Returns:
            所有响应列表
        """
        # TODO: 使用 asyncio.gather 并发请求
        # TODO: 通过 semaphore 控制并发
        ...

    def get_stats(self) -> dict:
        """获取请求统计"""
        return self._stats.copy()


# ==================== 测试 ====================
if __name__ == "__main__":
    async def main():
        client = AsyncHTTPClient(max_concurrent=5, rate_limit=10.0)

        # 并发请求多个测试 URL
        urls = [f"https://httpbin.org/delay/1" for _ in range(5)]
        start = time.time()
        responses = await client.fetch_many(urls)
        elapsed = time.time() - start

        for i, resp in enumerate(responses):
            print(f"  [{resp.status_code}] {resp.url}")
        print(f"总耗时: {elapsed:.2f}s")
        print(f"统计: {client.get_stats()}")

    asyncio.run(main())
