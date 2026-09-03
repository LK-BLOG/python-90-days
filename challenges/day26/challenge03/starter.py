"""
Challenge 03: Cookie 管理器 - CookieJar
"""
from typing import Dict, List, Optional
from datetime import datetime
from http.cookiejar import CookieJar, Cookie
import json


class CookieJar:
    """Cookie 管理器"""
    
    def __init__(self):
        self.cookies: Dict[str, Cookie] = {}
    
    def add(self, name: str, value: str, domain: str = "",
            path: str = "/", expires: datetime = None,
            secure: bool = False, http_only: bool = False):
        """添加 Cookie"""
        # TODO: 实现
        pass
    
    def get(self, name: str) -> Optional[str]:
        """获取 Cookie 值"""
        # TODO: 实现
        pass
    
    def remove(self, name: str):
        """删除 Cookie"""
        # TODO: 实现
        pass
    
    def parse_set_cookie(self, header: str):
        """解析 Set-Cookie 响应头"""
        # TODO: 实现
        # 格式: name=value; Path=/; Domain=.example.com; HttpOnly; Secure
        pass
    
    def get_cookie_header(self) -> str:
        """生成 Cookie 请求头"""
        # TODO: 实现
        pass
    
    def save(self, filepath: str):
        """保存到文件"""
        # TODO: 实现 JSON 格式保存
        pass
    
    def load(self, filepath: str):
        """从文件加载"""
        # TODO: 实现
        pass
    
    def clear(self):
        """清空所有 Cookie"""
        self.cookies.clear()
    
    def __len__(self):
        return len(self.cookies)
    
    def __contains__(self, name):
        return name in self.cookies


if __name__ == "__main__":
    jar = CookieJar()
    jar.add("session", "abc123")
    jar.add("user", "test")
    
    print(f"Cookie 数量: {len(jar)}")
    print(f"session: {jar.get('session')}")
    print(f"Cookie 头: {jar.get_cookie_header()}")
