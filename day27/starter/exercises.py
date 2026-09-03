"""
Day 27 练习：API 实战

请完成以下练习：
1. 使用 requests 调用 API
2. 封装 API 客户端
3. 处理分页
4. 错误处理和重试
"""

import requests
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time


# 练习 1：基础 API 调用

def fetch_json(url: str, params: Dict = None, headers: Dict = None) -> Any:
    """获取 JSON 数据
    
    TODO: 实现
    - 发送 GET 请求
    - 解析 JSON 响应
    - 处理错误
    """
    pass


def post_json(url: str, data: Dict, headers: Dict = None) -> Any:
    """发送 JSON 数据
    
    TODO: 实现
    - 发送 POST 请求
    - 解析响应
    - 处理错误
    """
    pass


# 练习 2：GitHub API 客户端

class GitHubClient:
    """GitHub API 客户端
    
    TODO: 实现以下功能
    - 获取用户信息
    - 获取仓库列表
    - 搜索仓库
    - 处理分页
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json"
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    
    def get_user(self, username: str) -> Dict:
        """获取用户信息"""
        # TODO: 实现
        pass
    
    def get_repos(self, username: str, page: int = 1, per_page: int = 10) -> List[Dict]:
        """获取用户仓库"""
        # TODO: 实现
        pass
    
    def search_repos(self, query: str, per_page: int = 10) -> Dict:
        """搜索仓库"""
        # TODO: 实现
        pass
    
    def get_all_repos(self, username: str) -> List[Dict]:
        """获取用户所有仓库（处理分页）"""
        # TODO: 实现分页获取
        pass


# 练习 3：分页处理器

class Paginator:
    """分页处理器
    
    TODO: 实现自动分页
    - 自动获取所有页面
    - 进度显示
    - 内存优化（生成器）
    """
    
    def __init__(self, client, method: str, path: str, **kwargs):
        self.client = client
        self.method = method
        self.path = path
        self.kwargs = kwargs
        self.page = 1
        self.per_page = kwargs.get("per_page", 30)
    
    def __iter__(self):
        """迭代所有页面"""
        # TODO: 实现
        pass
    
    def get_all(self) -> List:
        """获取所有数据"""
        # TODO: 实现
        pass


# 练习 4：重试机制

def retry_request(url: str, max_retries: int = 3, 
                  delay: float = 1.0, backoff: float = 2.0,
                  timeout: int = 30) -> requests.Response:
    """带重试的请求
    
    TODO: 实现
    - 失败自动重试
    - 指数退避
    - 超时控制
    """
    pass


# 练习 5：API 封装

class WeatherAPI:
    """天气 API 客户端
    
    TODO: 封装 OpenWeatherMap API（或使用 mock）
    - 获取当前天气
    - 获取预报
    - 错误处理
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current(self, city: str) -> Dict:
        """获取当前天气"""
        # TODO: 实现
        pass
    
    def get_forecast(self, city: str, days: int = 5) -> Dict:
        """获取天气预报"""
        # TODO: 实现
        pass


if __name__ == "__main__":
    print("Day 27 练习 - API 实战")
    
    # 测试基础 API 调用
    print("\n=== 基础 API ===")
    
    # 测试 GitHub 客户端
    print("\n=== GitHub 客户端 ===")
    client = GitHubClient()
    
    # 测试天气 API
    print("\n=== 天气 API ===")
