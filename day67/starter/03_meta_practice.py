# -*- coding: utf-8 -*-
"""Day 67：为文本块提取可检索元数据。"""
from typing import Any

class MetaPractice:
    """生成 source、标题、语言、长度等元数据。"""
    def extract(self, text: str, source: str | None = None) -> dict[str, Any]:
        """返回可与向量记录一起保存的元数据。"""
        if not isinstance(text, str) or not text.strip(): raise ValueError("文本不能为空")
        # TODO：添加标题、语言、章节、时间戳等字段
        return {"source": source or "unknown", "length": len(text), "language": "unknown"}

    def merge(self, base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
        """合并元数据，extra覆盖同名字段。"""
        # TODO：处理保留字段和嵌套元数据
        return {**base, **extra}

if __name__ == "__main__":
    print(MetaPractice().extract("一段文档", "guide.md"))
