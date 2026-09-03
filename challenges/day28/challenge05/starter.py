"""
Challenge 05: 异步爬虫框架 - AsyncCrawler
"""
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from collections import deque
from urllib.parse import urljoin, urlparse
import time


@dataclass
class CrawlResult:
    """爬取结果"""
    url: str
    status: int = 0
    data: Any = None
    error: str = None
    elapsed: float = 0.0
    links: List[str] = field(default_factory=list)


class AsyncCrawler:
    """异步爬虫框架"""
    
    def __init__(self, max_concurrent: int = 10, max_depth: int = 3,
                 timeout: float = 30.0, max_retries: int = 3):
        self.max_concurrent = max_concurrent
        self.max_depth = max_depth
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.visited = set()
        self.results: List[CrawlResult] = []
        self.semaphore = None
        self.session = None
        
        # 回调函数
        self.on_response: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
    
    async def __aenter__(self):
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        # TODO: 初始化 aiohttp session
        return self
    
    async def __aexit__(self, *args):
        # TODO: 关闭 session
        pass
    
    def add_url(self, url: str, depth: int = 0):
        """添加 URL 到队列"""
        # TODO: 实现
        pass
    
    async def fetch(self, url: str, depth: int = 0) -> CrawlResult:
        """爬取单个 URL"""
        # TODO: 实现
        # - 检查是否已访问
        # - 使用信号量
        # - 发送请求
        # - 解析响应
        # - 提取链接
        pass
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """提取链接"""
        # TODO: 实现
        # 简单的正则提取
        pass
    
    async def crawl(self, start_urls: List[str]) -> List[CrawlResult]:
        """开始爬取"""
        # TODO: 实现
        # - BFS 爬取
        # - 深度限制
        # - 并发控制
        pass
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        # TODO: 实现
        pass


if __name__ == "__main__":
    async def main():
        async with AsyncCrawler(max_concurrent=5, max_depth=2) as crawler:
            results = await crawler.crawl(["https://httpbin.org"])
            
            print(f"爬取完成: {len(results)} 个页面")
            print(f"统计: {crawler.get_stats()}")
    
    asyncio.run(main())
