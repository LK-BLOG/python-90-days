# Day 26 - Challenge 5: HTTP 客户端
# 难度: ⭐⭐⭐⭐
# 支持所有 HTTP 方法、Headers、Cookie/Session、认证、超时、重试

import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


@dataclass
class ClientConfig:
    """客户端配置"""
    base_url: str = ""
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    auth_type: str = "none"  # none / basic / bearer / api_key
    auth_credentials: dict[str, str] = field(default_factory=dict)


class SimpleHTTPClient:
    """简易 HTTP 客户端

    支持所有 HTTP 方法、认证、超时、重试、Cookie 管理。
    """

    def __init__(self, config: Optional[ClientConfig] = None):
        """初始化

        Args:
            config: 客户端配置
        """
        self.config = config or ClientConfig()
        # TODO: 初始化 Cookie 存储、认证管理器
        self._cookies: dict[str, str] = {}

    def request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        """发送 HTTP 请求（支持自动重试）

        Args:
            method: HTTP 方法
            path: 请求路径（相对于 base_url）
            **kwargs: 额外参数（headers, data, json, params）

        Returns:
            响应字典 {"status_code": ..., "headers": ..., "body": ...}

        Raises:
            HTTPError: 请求失败
            TimeoutError: 超时
        """
        # TODO: 拼接完整 URL
        # TODO: 添加认证头
        # TODO: 添加 Cookie
        # TODO: 构建 urllib Request 对象
        # TODO: 实现重试逻辑
        ...

    def get(self, path: str, **kwargs) -> dict[str, Any]:
        """GET 请求"""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> dict[str, Any]:
        """POST 请求"""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> dict[str, Any]:
        """PUT 请求"""
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> dict[str, Any]:
        """DELETE 请求"""
        return self.request("DELETE", path, **kwargs)

    def _build_url(self, path: str, params: dict = None) -> str:
        """构建完整 URL

        Args:
            path: 路径
            params: 查询参数

        Returns:
            完整 URL
        """
        # TODO: 拼接 base_url + path + 查询参数
        ...

    def _apply_auth(self, request_obj: Request) -> None:
        """应用认证头

        Args:
            request_obj: urllib Request 对象
        """
        # TODO: 根据 auth_type 添加对应的认证头
        ...

    def _apply_cookies(self, request_obj: Request) -> None:
        """应用 Cookie

        Args:
            request_obj: urllib Request 对象
        """
        # TODO: 从 _cookies 中筛选并添加 Cookie 头
        ...

    def _update_cookies(self, response) -> None:
        """从响应中更新 Cookie"""
        # TODO: 解析 Set-Cookie 头
        ...

    def _retry_with_backoff(self, func, max_retries: int) -> Any:
        """指数退避重试

        Args:
            func: 要执行的函数
            max_retries: 最大重试次数

        Returns:
            函数返回值
        """
        # TODO: 指数退避：delay * 2^attempt
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    client = SimpleHTTPClient(ClientConfig(
        base_url="https://httpbin.org",
        timeout=10,
        max_retries=2,
    ))
    try:
        resp = client.get("/get")
        print(f"状态码: {resp['status_code']}")
    except Exception as e:
        print(f"请求失败: {e}")
