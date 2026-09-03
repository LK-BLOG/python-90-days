"""
Challenge 04: 认证管理器 - AuthHandler
"""
from typing import Dict, Optional
import base64
from urllib.parse import urlencode


class AuthHandler:
    """认证管理器"""
    
    def __init__(self):
        self.auth_type = None
        self.credentials = {}
    
    def basic(self, username: str, password: str) -> 'AuthHandler':
        """设置 Basic 认证"""
        # TODO: 实现
        return self
    
    def bearer(self, token: str) -> 'AuthHandler':
        """设置 Bearer Token 认证"""
        # TODO: 实现
        return self
    
    def api_key(self, key: str, header: str = "X-API-Key") -> 'AuthHandler':
        """设置 API Key 认证"""
        # TODO: 实现
        return self
    
    def Session 持久化与状态管理2(self, client_id: str, client_secret: str) -> 'AuthHandler':
        """设置 Session 持久化与状态管理2 认证"""
        # TODO: 实现
        return self
    
    def get_headers(self) -> Dict[str, str]:
        """获取认证请求头"""
        # TODO: 实现
        pass
    
    def get_token(self, auth_server: str) -> Optional[str]:
        """获取 Session 持久化与状态管理 Token"""
        # TODO: 实现 Session 持久化与状态管理2 客户端凭证流程
        pass


if __name__ == "__main__":
    auth = AuthHandler()
    
    # Basic 认证
    auth.basic("admin", "password")
    print(f"Basic 头: {auth.get_headers()}")
    
    # Bearer Token
    auth.bearer("my_jwt_token")
    print(f"Bearer 头: {auth.get_headers()}")
    
    # API Key
    auth.api_key("my_api_key")
    print(f"API Key 头: {auth.get_headers()}")

