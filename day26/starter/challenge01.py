# Day 26 - Challenge 1: HTTP 请求构造器
# 难度: ⭐⭐
# 构建 GET/POST/PUT/DELETE 请求，支持自定义 Headers、查询参数、JSON/表单数据

import json
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlencode, urljoin


@dataclass
class HTTPRequest:
    """HTTP 请求对象"""
    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, str] = field(default_factory=dict)
    body: Any = None
    body_type: str = "none"  # none / json / form / raw


class HTTPRequestBuilder:
    """HTTP 请求构造器

    支持链式调用构建 HTTP 请求。
    """

    def __init__(self, base_url: str = ""):
        """初始化

        Args:
            base_url: 基础 URL
        """
        self._request = HTTPRequest(method="GET", url=base_url)

    def get(self, path: str = "") -> "HTTPRequestBuilder":
        """设置为 GET 请求

        Args:
            path: 请求路径

        Returns:
            self（支持链式调用）
        """
        self._request.method = "GET"
        self._request.url = urljoin(self._request.url, path)
        return self

    def post(self, path: str = "") -> "HTTPRequestBuilder":
        """设置为 POST 请求"""
        self._request.method = "POST"
        self._request.url = urljoin(self._request.url, path)
        return self

    def put(self, path: str = "") -> "HTTPRequestBuilder":
        """设置为 PUT 请求"""
        self._request.method = "PUT"
        self._request.url = urljoin(self._request.url, path)
        return self

    def delete(self, path: str = "") -> "HTTPRequestBuilder":
        """设置为 DELETE 请求"""
        self._request.method = "DELETE"
        self._request.url = urljoin(self._request.url, path)
        return self

    def header(self, key: str, value: str) -> "HTTPRequestBuilder":
        """添加请求头

        Args:
            key: 头部名
            value: 头部值
        """
        # TODO: 添加到 _request.headers
        ...

    def param(self, key: str, value: str) -> "HTTPRequestBuilder":
        """添加查询参数

        Args:
            key: 参数名
            value: 参数值
        """
        # TODO: 添加到 _request.params
        ...

    def json(self, data: Any) -> "HTTPRequestBuilder":
        """设置 JSON 请求体

        Args:
            data: JSON 数据（字典或列表）
        """
        # TODO: 设置 body 和 body_type，自动添加 Content-Type
        ...

    def form(self, data: dict[str, str]) -> "HTTPRequestBuilder":
        """设置表单请求体

        Args:
            data: 表单数据
        """
        # TODO: 设置 body 和 body_type，编码为 application/x-www-form-urlencoded
        ...

    def build(self) -> HTTPRequest:
        """构建最终的 HTTP 请求对象

        Returns:
            HTTPRequest 对象
        """
        # TODO: 拼接查询参数到 URL
        # TODO: 返回构建好的请求
        ...

    def to_raw(self) -> str:
        """导出为原始 HTTP 请求文本

        Returns:
            可直接发送的 HTTP 请求字符串
        """
        # TODO: 生成 GET /path HTTP/1.1\r\nHost: ...\r\n... 格式
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    req = (HTTPRequestBuilder("https://api.example.com")
           .get("/users")
           .param("page", "1")
           .param("limit", "10")
           .header("Accept", "application/json")
           .build())
    print(f"方法: {req.method}")
    print(f"URL: {req.url}")
    print(f"参数: {req.params}")
    print(f"请求头: {req.headers}")
