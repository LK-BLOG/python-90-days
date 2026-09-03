"""
Challenge 02: 响应解析器 - ResponseParser
"""
import json
from typing import Any, Dict, Optional
from io import BytesIO


class ResponseParser:
    """HTTP 响应解析器"""
    
    def __init__(self, status_code: int, reason: str = "",
                 headers: Dict[str, str] = None, body: bytes = b""):
        self.status_code = status_code
        self.reason = reason
        self.headers = headers or {}
        self.body = body
    
    def json(self) -> Any:
        """解析 JSON 响应"""
        # TODO: 实现
        pass
    
    def text(self, encoding: str = "utf-8") -> str:
        """解析文本响应"""
        # TODO: 实现
        pass
    
    @property
    def content(self) -> bytes:
        """获取原始内容"""
        return self.body
    
    @property
    def encoding(self) -> str:
        """检测编码"""
        # TODO: 从 Content-Type 或内容检测编码
        pass
    
    def raise_for_status(self):
        """检查状态码，失败则抛出异常"""
        # TODO: 实现
        pass


if __name__ == "__main__":
    # 示例使用
    response = ResponseParser(
        status_code=200,
        reason="OK",
        headers={"Content-Type": "application/json"},
        body=b'{"name": "test"}'
    )
    
    print(f"状态码: {response.status_code}")
    print(f"JSON: {response.json()}")
