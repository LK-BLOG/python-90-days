"""
Day 26 终极挑战：MiniRequests - 简化版 requests 库
"""
import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar
import json
import ssl
import time
import os
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from io import BytesIO


@dataclass
class Response:
    """HTTP 响应对象"""
    status_code: int
    headers: Dict[str, str]
    content: bytes
    url: str
    elapsed: float = 0.0
    encoding: str = "utf-8"
    
    def json(self) -> Any:
        """解析 JSON"""
        return json.loads(self.content)
    
    @property
    def text(self) -> str:
        """文本内容"""
        return self.content.decode(self.encoding)
    
    @property
    def ok(self) -> bool:
        """请求是否成功"""
        return 200 <= self.status_code < 400
    
    def raise_for_status(self):
        """失败则抛出异常"""
        if not self.ok:
            raise HTTPError(self.status_code, self.text, self)
    
    def __repr__(self):
        return f"<Response [{self.status_code}]>"


class HTTPError(Exception):
    """HTTP 错误"""
    def __init__(self, status_code: int, message: str, response: Response = None):
        self.status_code = status_code
        self.response = response
        super().__init__(f"HTTP {status_code}: {message}")


class Session:
    """HTTP 会话（支持 Cookie）"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "MiniRequests/1.0",
            "Accept": "application/json",
        }
        self.cookies = http.cookiejar.CookieJar()
        self.verify_ssl = True
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 1.0
        self._opener = None
    
    def _build_opener(self):
        """构建 URL opener"""
        # TODO: 实现
        # - Cookie 处理
        # - SSL 上下文
        pass
    
    def _prepare_request(self, method: str, url: str,
                         params: Dict = None, data: Any = None,
                         json_data: Any = None,
                         headers: Dict = None,
                         cookies: Dict = None) -> urllib.request.Request:
        """准备请求"""
        # TODO: 实现
        pass
    
    def request(self, method: str, url: str, **kwargs) -> Response:
        """发送请求"""
        # TODO: 实现
        # - 准备请求
        # - 发送请求
        # - 处理响应
        # - 重试机制
        pass
    
    def get(self, url: str, **kwargs) -> Response:
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Response:
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs) -> Response:
        return self.request("PUT", url, **kwargs)
    
    def patch(self, url: str, **kwargs) -> Response:
        return self.request("PATCH", url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Response:
        return self.request("DELETE", url, **kwargs)
    
    def head(self, url: str, **kwargs) -> Response:
        return self.request("HEAD", url, **kwargs)
    
    def options(self, url: str, **kwargs) -> Response:
        return self.request("OPTIONS", url, **kwargs)


def get(url: str, **kwargs) -> Response:
    """快捷 GET 请求"""
    with Session() as s:
        return s.get(url, **kwargs)


def post(url: str, **kwargs) -> Response:
    """快捷 POST 请求"""
    with Session() as s:
        return s.post(url, **kwargs)


if __name__ == "__main__":
    # 示例
    print("=== MiniRequests 测试 ===")
    
    # GET 请求
    response = get("https://httpbin.org/get")
    print(f"GET: {response.status_code}")
    print(response.json())
    
    # Session
    with Session() as s:
        s.get("https://httpbin.org/cookies/set?token=abc123")
        response = s.get("https://httpbin.org/cookies")
        print(f"\nCookies: {response.json()}")
