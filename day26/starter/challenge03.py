# Day 26 - Challenge 3: Cookie 管理器
# 难度: ⭐⭐⭐
# 从响应提取 Cookie、请求中添加、持久化、过期处理

import time
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from http.cookies import SimpleCookie


@dataclass
class Cookie:
    """单个 Cookie"""
    name: str
    value: str
    domain: str = ""
    path: str = "/"
    expires: float = 0.0  # Unix 时间戳，0 表示会话 Cookie
    secure: bool = False
    httponly: bool = False

    @property
    def is_expired(self) -> bool:
        """检查是否已过期"""
        # TODO: 如果 expires == 0 则为会话 Cookie（不过期）
        # TODO: 否则比较当前时间和 expires
        ...


class CookieManager:
    """Cookie 管理器

    管理 HTTP Cookie 的提取、添加、持久化和过期处理。
    """

    def __init__(self, storage_path: Optional[str] = None):
        """初始化

        Args:
            storage_path: Cookie 持久化文件路径，None 则不持久化
        """
        self.storage_path = Path(storage_path) if storage_path else None
        # TODO: 按域名存储 Cookie
        self._cookies: dict[str, list[Cookie]] = {}

    def extract_from_response(self, response_headers: dict[str, str],
                              domain: str = "") -> list[Cookie]:
        """从响应头中提取 Set-Cookie

        Args:
            response_headers: 响应头字典
            domain: Cookie 域名

        Returns:
            提取到的 Cookie 列表
        """
        # TODO: 从 Set-Cookie 头解析 Cookie
        # TODO: 处理 name=value; Path=...; Expires=...; Secure; HttpOnly
        ...

    def add_cookie(self, cookie: Cookie) -> None:
        """添加一个 Cookie

        Args:
            cookie: Cookie 对象
        """
        # TODO: 按域名分组存储，同名 Cookie 覆盖
        ...

    def get_cookies_for_url(self, url: str) -> dict[str, str]:
        """获取适用于指定 URL 的 Cookie

        Args:
            url: 目标 URL

        Returns:
            Cookie 键值对（可直接用于请求头）
        """
        # TODO: 筛选域名和路径匹配的 Cookie
        # TODO: 过滤已过期的 Cookie
        ...

    def add_to_headers(self, headers: dict[str, str], url: str) -> dict[str, str]:
        """将 Cookie 添加到请求头

        Args:
            headers: 现有请求头
            url: 目标 URL

        Returns:
            添加了 Cookie 的请求头
        """
        # TODO: 获取匹配的 Cookie，格式化为 Cookie: name1=val1; name2=val2
        ...

    def save(self) -> None:
        """持久化 Cookie 到文件"""
        # TODO: 将所有 Cookie 序列化为 JSON 并写入文件
        ...

    def load(self) -> None:
        """从文件加载 Cookie"""
        # TODO: 读取 JSON 文件，反序列化为 Cookie 对象
        ...

    def clear_expired(self) -> int:
        """清除所有过期 Cookie

        Returns:
            清除的 Cookie 数量
        """
        # TODO: 遍历所有 Cookie，移除已过期的
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    cm = CookieManager()
    # 模拟 Set-Cookie 响应头
    resp_headers = {
        "Set-Cookie": "session=abc123; Path=/; HttpOnly; Max-Age=3600"
    }
    cookies = cm.extract_from_response(resp_headers, domain="example.com")
    print(f"提取到 {len(cookies)} 个 Cookie")
    for c in cookies:
        print(f"  {c.name}={c.value}")
