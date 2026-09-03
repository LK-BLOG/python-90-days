"""
Day 26 练习：HTTP 协议基础

请完成以下练习：
1. 使用 urllib 发送 HTTP 请求
2. 处理响应
3. 管理 Cookie
4. 实现认证
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
from typing import Dict, Any, Optional


# 练习 1：HTTP 请求

def make_get_request(url: str, params: Dict[str, str] = None, 
                     headers: Dict[str, str] = None) -> Dict[str, Any]:
    """发送 GET 请求
    
    TODO: 实现 GET 请求
    - 处理查询参数
    - 自定义 Headers
    - 返回响应数据
    """
    pass


def make_post_request(url: str, data: Dict[str, Any] = None,
                      json_data: Dict[str, Any] = None,
                      headers: Dict[str, str] = None) -> Dict[str, Any]:
    """发送 POST 请求
    
    TODO: 实现 POST 请求
    - 支持表单数据
    - 支持 JSON 数据
    - 自定义 Headers
    """
    pass


def make_request_with_method(url: str, method: str = "GET",
                             data: Any = None,
                             headers: Dict[str, str] = None) -> Dict[str, Any]:
    """发送任意方法的请求
    
    TODO: 实现通用请求函数
    - 支持 GET/POST/PUT/DELETE
    - 统一的错误处理
    """
    pass


# 练习 2：响应处理

def check_response_status(response) -> bool:
    """检查响应状态
    
    TODO: 实现状态码检查
    - 2xx 返回 True
    - 其他返回 False 或抛出异常
    """
    pass


def parse_json_response(response) -> Any:
    """解析 JSON 响应
    
    TODO: 实现 JSON 解析
    - 处理编码问题
    - 处理解析错误
    """
    pass


# 练习 3：Cookie 管理

class CookieManager:
    """Cookie 管理器
    
    TODO: 实现以下功能
    - 从响应中提取 Cookie
    - 在请求中添加 Cookie
    - Cookie 持久化
    """
    
    def __init__(self):
        self.cookies = {}
    
    def add_cookie(self, name: str, value: str, **kwargs):
        """添加 Cookie"""
        pass
    
    def get_cookie(self, name: str) -> Optional[str]:
        """获取 Cookie"""
        pass
    
    def remove_cookie(self, name: str):
        """删除 Cookie"""
        pass
    
    def get_cookie_header(self) -> str:
        """获取 Cookie 请求头"""
        pass
    
    def parse_set_cookie(self, set_cookie_header: str):
        """解析 Set-Cookie 响应头"""
        pass
    
    def save(self, filepath: str):
        """保存 Cookie 到文件"""
        pass
    
    def load(self, filepath: str):
        """从文件加载 Cookie"""
        pass


# 练习 4：认证

class AuthManager:
    """认证管理器
    
    TODO: 实现以下认证方式
    - Basic 认证
    - Bearer Token
    - API Key
    """
    
    def __init__(self):
        self.auth_type = None
        self.credentials = {}
    
    def basic_auth(self, username: str, password: str):
        """设置 Basic 认证"""
        pass
    
    def bearer_token(self, token: str):
        """设置 Bearer Token"""
        pass
    
    def api_key(self, key: str, header: str = "X-API-Key"):
        """设置 API Key"""
        pass
    
    def get_auth_header(self) -> Dict[str, str]:
        """获取认证请求头"""
        pass


# 练习 5：HTTP 客户端

class SimpleHTTPClient:
    """简单的 HTTP 客户端
    
    TODO: 实现完整的 HTTP 客户端
    - 支持所有 HTTP 方法
    - Cookie 管理
    - 认证支持
    - 错误处理
    - 超时控制
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.cookie_manager = CookieManager()
        self.auth_manager = AuthManager()
        self.headers = {"User-Agent": "SimpleHTTPClient/1.0"}
    
    def get(self, path: str = "", params: Dict = None, **kwargs):
        """GET 请求"""
        pass
    
    def post(self, path: str = "", data: Dict = None, **kwargs):
        """POST 请求"""
        pass
    
    def put(self, path: str = "", data: Dict = None, **kwargs):
        """PUT 请求"""
        pass
    
    def delete(self, path: str = "", **kwargs):
        """DELETE 请求"""
        pass
    
    def _build_url(self, path: str, params: Dict = None) -> str:
        """构建完整 URL"""
        pass
    
    def _request(self, url: str, method: str = "GET",
                 data: Any = None, **kwargs) -> Dict[str, Any]:
        """发送请求"""
        pass


if __name__ == "__main__":
    print("Day 26 练习 - HTTP 协议")
    
    # 测试 GET 请求
    print("\n=== GET 请求 ===")
    
    # 测试 POST 请求
    print("\n=== POST 请求 ===")
    
    # 测试 Cookie 管理
    print("\n=== Cookie 管理 ===")
    
    # 测试认证
    print("\n=== 认证 ===")
    
    # 测试 HTTP 客户端
    print("\n=== HTTP 客户端 ===")
