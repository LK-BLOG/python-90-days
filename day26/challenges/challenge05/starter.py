"""
Challenge 05: HTTP 客户端 - HttpClient
"""
import urllib.request
import urllib.error
import urllib.parse
import json
import ssl
import time
from typing import Dict, Any, Optional


class HTTPError(Exception):
    """HTTP 错误"""
    def __init__(self, status_code: int, reason: str, response=None):
        self.status_code = status_code
        self.reason = reason
        self.response = response
        super().__init__(f"HTTP {status_code}: {reason}")


class Response:
    """HTTP 响应"""
    
    def __init__(self, status_code: int, headers: Dict, data: bytes):
        self.status_code = status_code
        self.headers = headers
        self.data = data
    
    def json(self) -> Any:
        return json.loads(self.data)
    
    @property
    def text(self) -> str:
        return self.data.decode("utf-8")
    
    @property
    def content(self) -> bytes:
        return self.data
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise HTTPError(self.status_code, "Error", self)


class HttpClient:
    """HTTP 客户端"""
    
    def __init__(self, base_url: str = "", timeout: int = 30,
                 verify_ssl: bool = True):
        self.base_url = base_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.headers = {"User-Agent": "HttpClient/1.0"}
        self.cookies = {}
        self.auth = None
    
    def get(self, path: str = "", params: Dict = None, **kwargs) -> Response:
        """GET 请求"""
        # TODO: 实现
        pass
    
    def post(self, path: str = "", data: Any = None, json_data: Any = None,
             **kwargs) -> Response:
        """POST 请求"""
        # TODO: 实现
        pass
    
    def put(self, path: str = "", data: Any = None, **kwargs) -> Response:
        """PUT 请求"""
        # TODO: 实现
        pass
    
    def delete(self, path: str = "", **kwargs) -> Response:
        """DELETE 请求"""
        # TODO: 实现
        pass
    
    def _request(self, method: str, path: str, **kwargs) -> Response:
        """发送请求"""
        # TODO: 实现
        # - 构建 URL
        # - 设置 Headers
        # - 处理 Cookie
        # - 处理认证
        # - 发送请求
        # - 处理响应
        # - 重试机制
        pass
    
    def _build_url(self, path: str, params: Dict = None) -> str:
        """构建完整 URL"""
        # TODO: 实现
        pass


if __name__ == "__main__":
    client = HttpClient("https://httpbin.org")
    
    # GET 请求
    response = client.get("/get", params={"key": "value"})
    print(f"GET 响应: {response.status_code}")
    print(response.json())
    
    # POST 请求
    response = client.post("/post", json_data={"name": "test"})
    print(f"\nPOST 响应: {response.status_code}")
    print(response.json())
