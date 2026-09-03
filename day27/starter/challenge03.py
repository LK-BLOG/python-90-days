# Day 27 - Challenge 3: API 封装框架
# 难度: ⭐⭐⭐
# 统一请求方法、自动认证、重试机制、速率限制、日志记录

import time
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError


logger = logging.getLogger(__name__)


@dataclass
class RateLimiter:
    """速率限制器"""
    max_requests: int = 60
    window_seconds: float = 60.0
    _timestamps: list[float] = field(default_factory=list)

    def wait_if_needed(self) -> float:
        """检查是否需要等待，返回等待时间

        Returns:
            实际等待的秒数
        """
        # TODO: 清理窗口外的时间戳
        # TODO: 如果达到上限，计算等待时间
        ...


class APIClient:
    """API 客户端框架

    提供统一的 API 调用接口，内置认证、重试、限流、日志。
    """

    def __init__(self, base_url: str, auth_token: Optional[str] = None,
                 max_retries: int = 3, rate_limit: int = 60):
        """初始化

        Args:
            base_url: API 基础 URL
            auth_token: 认证令牌
            max_retries: 最大重试次数
            rate_limit: 每分钟最大请求数
        """
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.max_retries = max_retries
        self._rate_limiter = RateLimiter(max_requests=rate_limit)
        # TODO: 初始化重试策略和请求统计
        self._stats: dict[str, int] = {"total": 0, "success": 0, "failed": 0}

    def _build_request(self, method: str, path: str,
                       headers: dict = None, data: Any = None) -> Request:
        """构建请求对象

        Args:
            method: HTTP 方法
            path: API 路径
            headers: 额外请求头
            data: 请求体

        Returns:
            urllib Request 对象
        """
        # TODO: 拼接 URL，添加认证头，设置请求体
        ...

    def request(self, method: str, path: str, **kwargs) -> dict:
        """发送请求（带重试和限流）

        Args:
            method: HTTP 方法
            path: API 路径
            **kwargs: headers, data, json, params

        Returns:
            响应数据
        """
        # TODO: 等待速率限制
        # TODO: 带重试的请求发送
        # TODO: 记录日志和统计
        ...

    def get(self, path: str, **kwargs) -> dict:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> dict:
        return self.request("POST", path, **kwargs)

    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """指数退避重试

        Args:
            func: 可调用对象
        """
        # TODO: 捕获 HTTPError，429/5xx 时重试
        # TODO: 指数退避 delay = base * 2^attempt
        ...

    def get_stats(self) -> dict:
        """获取请求统计"""
        return self._stats.copy()


# ==================== 测试 ====================
if __name__ == "__main__":
    client = APIClient("https://api.example.com", max_retries=2)
    print(f"API 客户端初始化: {client.base_url}")
    print("统计:", client.get_stats())
