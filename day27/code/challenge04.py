"""
Challenge 04: 分页处理器 - PageFetcher
"""
from typing import Dict, List, Any, Optional, Callable, Iterator
import requests


class PageFetcher:
    """分页数据获取器"""
    
    def __init__(self, client: requests.Session, url: str,
                 params: Dict = None, per_page: int = 30,
                 max_pages: int = 100):
        self.client = client
        self.url = url
        self.params = params or {}
        self.per_page = per_page
        self.max_pages = max_pages
    
    def fetch_page(self, page: int) -> Dict:
        """获取单页数据"""
        # TODO: 实现
        pass
    
    def get_total_pages(self) -> int:
        """获取总页数"""
        # TODO: 实现
        pass
    
    def iterate_pages(self) -> Iterator[List[Dict]]:
        """迭代所有页面（生成器）"""
        # TODO: 实现
        # 逐页获取，内存友好
        pass
    
    def fetch_all(self) -> List[Dict]:
        """获取所有数据"""
        # TODO: 实现
        pass
    
    def fetch_with_progress(self, callback: Callable = None) -> List[Dict]:
        """带进度回调的获取"""
        # TODO: 实现
        pass
