"""示例4：API 封装最佳实践"""
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """API 配置"""
    base_url: str
    timeout: int = 30
    max_retries: int = 3
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


class APIClient:
    """API 客户端基类"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.headers)
        self.session.timeout = config.timeout
    
    def _request(self, method: str, path: str, **kwargs) -> Dict:
        """发送请求"""
        url = f"{self.config.base_url}{path}"
        
        try:
            logger.info(f"{method.upper()} {url}")
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 错误: {e.response.status_code}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
            raise
    
    def get(self, path: str, params: Dict = None, **kwargs) -> Dict:
        """GET 请求"""
        return self._request("GET", path, params=params, **kwargs)
    
    def post(self, path: str, data: Any = None, **kwargs) -> Dict:
        """POST 请求"""
        return self._request("POST", path, json=data, **kwargs)
    
    def put(self, path: str, data: Any = None, **kwargs) -> Dict:
        """PUT 请求"""
        return self._request("PUT", path, json=data, **kwargs)
    
    def delete(self, path: str, **kwargs) -> Dict:
        """DELETE 请求"""
        return self._request("DELETE", path, **kwargs)


class GitHubClient(APIClient):
    """GitHub API 客户端"""
    
    def __init__(self, token: str = None):
        config = APIConfig(
            base_url="https://api.github.com",
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "PythonGitHubClient/1.0"
            }
        )
        super().__init__(config)
        
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    
    def get_user(self, username: str) -> Dict:
        """获取用户信息"""
        return self.get(f"/users/{username}")
    
    def get_repos(self, username: str, per_page: int = 10) -> List[Dict]:
        """获取用户仓库"""
        return self.get(f"/users/{username}/repos",
                       params={"per_page": per_page, "sort": "stars"})
    
    def search_repos(self, query: str, per_page: int = 10) -> Dict:
        """搜索仓库"""
        return self.get("/search/repositories",
                       params={"q": query, "per_page": per_page})


if __name__ == "__main__":
    # 使用
    client = GitHubClient()
    
    # 获取用户
    user = client.get_user("octocat")
    print(f"用户: {user['login']}")
    print(f"仓库数: {user['public_repos']}")
    
    # 获取仓库
    repos = client.get_repos("octocat", per_page=5)
    print("\n热门仓库:")
    for repo in repos:
        print(f"  {repo['name']}: ⭐{repo['stargazers_count']}")
    
    # 搜索
    results = client.search_repos("python", per_page=5)
    print(f"\n搜索结果: {results['total_count']} 个仓库")
