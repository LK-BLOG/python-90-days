# Day 26 - Challenge 4: 认证管理器
# 难度: ⭐⭐⭐
# Basic 认证、Bearer Token、API Key、Session 持久化

import base64
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


class AuthManager:
    """认证管理器

    支持多种认证方式的统一管理。
    """

    def __init__(self, session_path: Optional[str] = None):
        """初始化

        Args:
            session_path: Session 持久化路径
        """
        self.session_path = Path(session_path) if session_path else None
        # TODO: 存储认证状态
        self._auth_type: str = "none"
        self._credentials: dict[str, str] = {}

    def basic_auth(self, username: str, password: str) -> dict[str, str]:
        """生成 Basic 认证头

        Args:
            username: 用户名
            password: 密码

        Returns:
            包含 Authorization 头的字典
        """
        # TODO: base64 编码 "username:password"
        # TODO: 返回 {"Authorization": "Basic xxx"}
        ...

    def bearer_token(self, token: str) -> dict[str, str]:
        """生成 Bearer Token 认证头

        Args:
            token: 访问令牌

        Returns:
            包含 Authorization 头的字典
        """
        # TODO: 返回 {"Authorization": "Bearer xxx"}
        ...

    def api_key(self, key: str, header_name: str = "X-API-Key") -> dict[str, str]:
        """生成 API Key 认证头

        Args:
            key: API 密钥
            header_name: 密钥放在哪个请求头

        Returns:
            包含 API Key 头的字典
        """
        # TODO: 返回 {header_name: key}
        ...

    def get_auth_headers(self) -> dict[str, str]:
        """获取当前认证方式对应的请求头

        Returns:
            认证相关请求头
        """
        # TODO: 根据当前认证类型生成请求头
        ...

    def save_session(self) -> None:
        """保存当前 Session 到文件"""
        # TODO: 序列化认证状态到 JSON 文件
        ...

    def load_session(self) -> bool:
        """从文件加载 Session

        Returns:
            是否成功加载
        """
        # TODO: 读取 JSON 文件，恢复认证状态
        # TODO: 检查 token 是否过期
        ...

    def refresh_token(self) -> bool:
        """刷新过期的 Token

        Returns:
            是否刷新成功
        """
        # TODO: 如果有 refresh_token，用它获取新的 access_token
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    auth = AuthManager()

    # Basic 认证
    headers = auth.basic_auth("admin", "secret123")
    print(f"Basic Auth: {headers}")

    # Bearer Token
    headers = auth.bearer_token("eyJhbGciOiJIUzI1NiJ9...")
    print(f"Bearer: {headers}")

    # API Key
    headers = auth.api_key("sk-xxx123")
    print(f"API Key: {headers}")
