# Day 17 - Challenge 5: 序列化系统
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 用 asdict 和 JSON 实现序列化
# 参考 challenge.md

"""
序列化系统挑战 — dataclass 与 JSON 序列化/反序列化

核心知识点:
- dataclasses.asdict()
- 自定义序列化
- 日期时间序列化
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import Any, Optional


# ===== 自定义 JSON 编解码器 =====

class DataclassEncoder(json.JSONEncoder):
    """自定义 JSON 编码器 — 支持 dataclass 和 datetime"""

    def default(self, obj: Any) -> Any:
        # TODO: 处理以下类型:
        # 1. dataclass 实例 -> asdict(obj)
        # 2. datetime -> isoformat()
        # 3. date -> isoformat()
        # 4. set -> sorted list
        pass


class DataclassDecoder:
    """JSON 解码器 — 支持还原 dataclass"""

    _registry: dict = {}  # 类名 -> 类 的映射

    @classmethod
    def register(cls, *dataclasses):
        """注册需要反序列化的 dataclass"""
        for dc in dataclasses:
            cls._registry[dc.__name__] = dc

    @classmethod
    def decode(cls, json_str: str) -> Any:
        """解码 JSON 为 dataclass 实例"""
        data = json.loads(json_str)
        # TODO: 递归还原 dataclass
        pass


# ===== 数据模型 =====

@dataclass
class Tag:
    """标签"""
    name: str
    color: str = "#333333"


@dataclass
class Article:
    """文章 — 完整序列化示例"""
    title: str
    content: str
    author: str
    tags: list[Tag] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    published: bool = False
    views: int = 0

    def to_json(self, indent: int = 2) -> str:
        """序列化为 JSON"""
        return json.dumps(asdict(self), cls=DataclassEncoder, indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "Article":
        """从 JSON 反序列化"""
        # TODO: 解析 JSON -> 递归还原嵌套的 dataclass
        pass

    def to_summary(self) -> dict:
        """生成摘要字典"""
        return {
            "title": self.title,
            "author": self.author,
            "tags": [t.name for t in self.tags],
            "published": self.published,
        }


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 序列化系统测试 ===")

    art = Article(
        title="Python Dataclass",
        content="详解 dataclass 的用法",
        author="小戡",
        tags=[Tag("Python"), Tag("教程", "#ff6600")],
        published=True,
    )

    # 序列化
    json_str = art.to_json()
    print(f"JSON:\n{json_str[:200]}...")

    # 摘要
    print(f"摘要: {art.to_summary()}")

    # asdict 演示
    d = asdict(art)
    print(f"asdict keys: {list(d.keys())}")

    print("✅ Challenge 05 完成")
