"""
Challenge 03: 异步 HTTP 客户端 - AsyncHttpClient
"""
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class Response:
    """HTTP 响应"""
    status: int
    headers: Dict[str, str]
    data: bytes
    
    def json(self):
        import json
        return json.loads(self.data)
    
    @property
    def text(self) -> str:
        return self.data.decode("utf-8")


class AsyncHttpClient:
    """异步 HTTP 客户端"""
    
    def __init__(self, base_url: str = "", max_concurrent: int = 10,
                 timeout: float = 30.0, max_retries: int = 3):
        self.base_url = base_url
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.max_retries = max_retries
        self.semaphore = None
        self.session = None
    
    async def __aenter__(self):
        # TODO: 初始化 aiohttp session
        return self
    
    async def __aexit__(self, *args):
        # TODO: 关闭 session
        pass
    
    async def get(self, path: str = "", params: Dict = None, **kwargs) -> Response:
        """GET 请求"""
        # TODO: 实现
        pass
    
    async def post(self, path: str = "", data: Any = None, **kwargs) -> Response:
        """POST 请求"""
        # TODO: 实现
        pass
    
    async def fetch_all(self, requests: List[Dict]) -> List[Response]:
        """并发获取多个 URL"""
        # TODO: 实现
        # 使用 Semaphore 限制并发
        pass
    
    async def _request_with_retry(self, method: str, url: str, **kwargs) -> Response:
        """带重试的请求"""
        # TODO: 实现
        pass


if __name__ == "__main__":
    async def main():
        async with AsyncHttpClient("https://httpbin.org") as client:
            # 单个请求
            response = await client.get("/get")
            print(f"状态: {response.status}")
            
            # 并发请求
            requests = [
                {"method": "GET", "path": f"/get?id={i}"}
                for i in range(10)
            ]
            responses = await client.fetch_all(requests)
            print(f"完成 {len(responses)} 个请求")
    
    asyncio.run(main())
