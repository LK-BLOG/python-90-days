# -*- coding: utf-8 -*-
"""Day 64：解析模型的工具调用响应。"""
import json
from typing import Any

class ParserPractice:
    """把模型返回的文本解析为可执行的工具调用。"""
    def parse(self, response: str) -> dict[str, Any]:
        """解析JSON响应，要求包含 name 和 arguments 字段。"""
        if not isinstance(response, str) or not response.strip():
            raise ValueError("模型响应不能为空")
        # TODO：处理纯JSON、Markdown代码块和非法JSON三种情况
        data = json.loads(response)
        if not isinstance(data, dict) or "name" not in data:
            raise ValueError("响应缺少工具名称")
        data.setdefault("arguments", {})
        return data

    def validate_call(self, call: dict[str, Any], allowed: set[str]) -> bool:
        """验证工具名和参数结构，防止调用未注册工具。"""
        # TODO：补充参数类型和必填字段检查
        return call.get("name") in allowed and isinstance(call.get("arguments"), dict)

if __name__ == "__main__":
    parser = ParserPractice()
    print(parser.parse('{"name": "search", "arguments": {"query": "python"}}'))
