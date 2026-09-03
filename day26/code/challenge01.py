"""
Challenge 01: HTTP 请求构造器 - RequestBuilder
"""
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import json


class RequestBuilder:
    """HTTP 请求构造器"""
    
    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self.method = "GET"
        self.path = ""
        self.headers = {}
        self.params = {}
        self.body = None
        self.content_type = None
    
    def set_method(self, method: str) -> 'RequestBuilder':
        """设置 HTTP 方法"""
        # TODO: 实现
        return self
    
    def set_path(self, path: str) -> 'RequestBuilder':
        """设置路径"""
        # TODO: 实现
        return self
    
    def add_header(self, key: str, value: str) -> 'RequestBuilder':
        """添加请求头"""
        # TODO: 实现
        return self
    
    def set_params(self, params: Dict[str, str]) -> 'RequestBuilder':
        """设置查询参数"""
        # TODO: 实现
        return self
    
    def set_json(self, data: Dict[str, Any]) -> 'RequestBuilder':
        """设置 JSON 请求体"""
        # TODO: 实现
        return self
    
    def set_form(self, data: Dict[str, str]) -> 'RequestBuilder':
        """设置表单请求体"""
        # TODO: 实现
        return self
    
    def build_url(self) -> str:
        """构建完整 URL"""
        # TODO: 实现
        pass
    
    def preview(self) -> str:
        """预览请求"""
        # TODO: 返回可读的请求描述
        pass


if __name__ == "__main__":
    builder = RequestBuilder("https://api.example.com")
    request = (builder
               .set_method("POST")
               .set_path("/users")
               .add_header("Accept", "application/json")
               .set_json({"name": "张三", "email": "test@example.com"})
               .preview())
    print(request)
