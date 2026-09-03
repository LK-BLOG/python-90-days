"""
Challenge 03: API 封装框架 - ApiClient
"""
import requests
import time
import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps


class ApiClient:
    """通用 API 客户端"""
    
    def __init__(self, base_url: str, timeout: int = 30,
                 max_retries: int = 3, rate_limit: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit  # 最小请求间隔（秒）
        self.session = requests.Session()
        self._last_request_time = 0
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _throttle(self):
        """速率限制"""
        # TODO: 实现
        pass
    
    def _request(self, method: str, path: str, **kwargs) -> Dict:
        """发送请求（带重试）"""
        # TODO: 实现
        # - 速率限制
        # - 重试机制
        # - 错误处理
        # - 日志记录
        pass
    
    def get(self, path: str, params: Dict = None, **kwargs) -> Dict:
        return self._request("GET", path, params=params, **kwargs)
    
    def post(self, path: str, data: Any = None, **kwargs) -> Dict:
        return self._request("POST", path, json=data, **kwargs)
    
    def put(self, path: str, data: Any = None, **kwargs) -> Dict:
        return self._request("PUT", path, json=data, **kwargs)
    
    def delete(self, path: str, **kwargs) -> Dict:
        return self._request("DELETE", path, **kwargs)
