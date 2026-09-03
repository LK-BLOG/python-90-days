# Day 26 - Challenge 2: 响应解析器
# 难度: ⭐⭐
# 解析状态码、响应头、JSON/HTML/文本、编码处理

import json
from dataclasses import dataclass, field
from typing import Any
from email.message import Message


@dataclass
class HTTPResponse:
    """HTTP 响应对象"""
    status_code: int = 0
    reason: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    raw_body: bytes = b""
    encoding: str = "utf-8"


class HTTPResponseParser:
    """HTTP 响应解析器

    解析原始 HTTP 响应为结构化对象。
    """

    # 状态码 -> 原因短语映射
    STATUS_PHRASES: dict[int, str] = {
        200: "OK",
        201: "Created",
        301: "Moved Permanently",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def parse_raw(self, raw_response: bytes) -> HTTPResponse:
        """解析原始 HTTP 响应

        Args:
            raw_response: 原始响应字节

        Returns:
            HTTPResponse 对象
        """
        # TODO: 按 \r\n\r\n 分割头部和体
        # TODO: 解析状态行：HTTP/1.1 200 OK
        # TODO: 解析响应头
        # TODO: 解码响应体
        ...

    def parse_headers(self, header_text: str) -> dict[str, str]:
        """解析响应头文本

        Args:
            header_text: 头部文本块

        Returns:
            头部键值对字典
        """
        # TODO: 按行分割，按 : 分割键值
        # TODO: 处理多值头部
        ...

    def get_json(self, response: HTTPResponse) -> Any:
        """解析 JSON 响应体

        Args:
            response: HTTP 响应对象

        Returns:
            解析后的 Python 对象

        Raises:
            json.JSONDecodeError: JSON 格式错误
        """
        # TODO: 检查 Content-Type，使用 response.encoding 解码后 json.loads
        ...

    def get_text(self, response: HTTPResponse) -> str:
        """获取文本形式的响应体

        Args:
            response: HTTP 响应对象

        Returns:
            解码后的文本
        """
        # TODO: 使用正确的编码解码 raw_body
        ...

    def detect_encoding(self, response: HTTPResponse) -> str:
        """从 Content-Type 或内容中检测编码

        Args:
            response: HTTP 响应对象

        Returns:
            编码名称
        """
        # TODO: 优先从 Content-Type 的 charset 参数获取
        # TODO: 回退到 chardet 检测或默认 utf-8
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    # 模拟一个 HTTP 响应
    raw = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json; charset=utf-8\r\n"
        b"Content-Length: 27\r\n"
        b"\r\n"
        b'{"message": "Hello, World!"}'
    )
    parser = HTTPResponseParser()
    resp = parser.parse_raw(raw)
    print(f"状态码: {resp.status_code}")
    print(f"JSON: {parser.get_json(resp)}")
