# Day 26 - Boss Challenge: 完整 HTTP 客户端库
# 难度: ⭐⭐⭐⭐⭐
# 类似 requests 的简化版 HTTP 客户端

import json
import ssl
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError


@dataclass
class Response:
    """HTTP 响应"""
    status_code: int = 0
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    elapsed_ms: float = 0.0
    encoding: str = "utf-8"

    def json(self) -> Any:
        """解析 JSON 响应体"""
        return json.loads(self.body.decode(self.encoding))

    @property
    def text(self) -> str:
        """文本响应体"""
        return self.body.decode(self.encoding)

    @property
    def ok(self) -> bool:
        """请求是否成功（2xx）"""
        return 200 <= self.status_code < 300


@dataclass
class Session:
    """会话管理，跨请求保持状态"""
    cookies: dict[str, str] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    auth: tuple[str, str] | None = None
    verify_ssl: bool = True
    timeout: int = 30


class MiniRequests:
    """Mini Requests 库

    简化版 HTTP 客户端，支持：
    - 所有 HTTP 方法
    - Headers / Cookie / Session
    - 多种认证方式
    - SSL / 代理
    - 超时和重试
    - 文件上传/下载
    """

    def __init__(self):
        self.session = Session()
        self._hooks: dict[str, list[Callable]] = {"response": []}

    def get(self, url: str, **kwargs) -> Response:
        """GET 请求"""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        """POST 请求"""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        """PUT 请求"""
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs) -> Response:
        """PATCH 请求"""
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        """DELETE 请求"""
        return self.request("DELETE", url, **kwargs)

    def request(self, method: str, url: str, **kwargs) -> Response:
        """发送请求

        Args:
            method: HTTP 方法
            url: 完整 URL
            **kwargs: headers, data, json, params, timeout, auth

        Returns:
            Response 对象
        """
        # TODO: 合并 session 默认 headers 和 kwargs headers
        # TODO: 处理 params -> URL 拼接
        # TODO: 处理 json -> body + Content-Type
        # TODO: 处理认证
        # TODO: 发送请求并计时
        # TODO: 更新 session cookies
        # TODO: 执行 hooks
        ...

    def upload(self, url: str, file_path: str, field_name: str = "file",
               **kwargs) -> Response:
        """上传文件

        Args:
            url: 上传地址
            file_path: 文件路径
            field_name: 表单字段名
        """
        # TODO: 读取文件，构建 multipart/form-data
        ...

    def download(self, url: str, save_path: str, chunk_size: int = 8192) -> Path:
        """下载文件

        Args:
            url: 下载地址
            save_path: 保存路径
            chunk_size: 分块大小
        """
        # TODO: 流式下载，写入文件
        ...

    def register_hook(self, event: str, callback: Callable) -> None:
        """注册事件钩子"""
        # TODO: 注册 response 事件回调
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    client = MiniRequests()
    resp = client.get("https://httpbin.org/get")
    print(f"状态码: {resp.status_code}")
    print(f"成功: {resp.ok}")
