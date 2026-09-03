"""
Challenge 01: GitHub API 客户端 - GitHubExplorer
"""
import requests
import json
from typing import Dict, List, Optional


class GitHubExplorer:
    """GitHub 探索器"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json"
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    
    def explore_user(self, username: str) -> Dict:
        """探索用户信息"""
        # TODO: 获取用户信息
        # TODO: 获取热门仓库
        # TODO: 生成摘要
        pass
    
    def trending_repos(self, language: str = "python", since: str = "daily") -> List[Dict]:
        """获取热门仓库"""
        # TODO: 实现
        pass
    
    def user_activity(self, username: str) -> List[Dict]:
        """获取用户活动"""
        # TODO: 实现
        pass


if __name__ == "__main__":
    explorer = GitHubExplorer()
    info = explorer.explore_user("octocat")
    print(json.dumps(info, indent=2))
