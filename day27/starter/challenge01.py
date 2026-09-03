# Day 27 - Challenge 1: GitHub API 客户端
# 难度: ⭐⭐
# 获取用户信息、仓库列表、搜索仓库、分页、错误处理

import json
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class GitHubClient:
    """GitHub API 客户端

    封装 GitHub REST API，支持用户查询、仓库列表、搜索等功能。
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """初始化

        Args:
            token: GitHub Personal Access Token（可选）
        """
        self.token = token
        # TODO: 设置默认请求头

    def _request(self, endpoint: str, params: dict = None) -> Any:
        """发送 API 请求

        Args:
            endpoint: API 端点（如 /users/octocat）
            params: 查询参数

        Returns:
            解析后的 JSON 数据

        Raises:
            HTTPError: API 请求失败
        """
        # TODO: 拼接 URL，添加认证头，发送请求
        ...

    def get_user(self, username: str) -> dict:
        """获取用户信息

        Args:
            username: GitHub 用户名

        Returns:
            用户信息字典
        """
        # TODO: GET /users/{username}
        ...

    def get_user_repos(self, username: str, per_page: int = 30,
                       page: int = 1) -> list[dict]:
        """获取用户的仓库列表

        Args:
            username: 用户名
            per_page: 每页数量
            page: 页码

        Returns:
            仓库信息列表
        """
        # TODO: GET /users/{username}/repos
        ...

    def search_repos(self, query: str, sort: str = "stars",
                     per_page: int = 10) -> dict:
        """搜索仓库

        Args:
            query: 搜索关键词
            sort: 排序方式（stars/forks/updated）
            per_page: 每页数量

        Returns:
            搜索结果（含 total_count 和 items）
        """
        # TODO: GET /search/repositories?q={query}&sort={sort}
        ...

    def get_all_user_repos(self, username: str) -> list[dict]:
        """获取用户的所有仓库（自动分页）

        Args:
            username: 用户名

        Returns:
            完整的仓库列表
        """
        # TODO: 循环分页获取所有仓库
        ...

    def handle_rate_limit(self, response_headers: dict) -> dict:
        """检查 API 速率限制

        Args:
            response_headers: 响应头

        Returns:
            速率限制信息 {"limit": ..., "remaining": ..., "reset": ...}
        """
        # TODO: 解析 X-RateLimit-* 头
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    client = GitHubClient()
    try:
        user = client.get_user("octocat")
        print(f"用户: {user.get('login', 'N/A')}")
        print(f"公开仓库: {user.get('public_repos', 'N/A')}")
    except Exception as e:
        print(f"API 请求失败: {e}")
