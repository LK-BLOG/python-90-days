# Day 12 - Challenge 4: 包文档
# 难度: ⭐⭐⭐☆☆
#
# 要求: 为包编写完整的文档，包括 docstring、README、API 文档
# 参考 challenge.md

"""
包文档挑战 — 学会为 Python 包编写规范的文档

核心知识点:
- 模块级 docstring
- 函数/类 docstring (Google/NumPy 风格)
- 类型注解
- README 撰写
"""

from typing import Any


# ===== 模块级 docstring 示例 =====
"""
my_toolkit.string_utils — 字符串工具集

本模块提供常用的字符串处理函数。

使用示例::

    from my_toolkit.string_utils import slugify, truncate

    slug = slugify("Hello World!")
    # => "hello-world"

    short = truncate("很长的文本...", max_len=10)
"""


class TextProcessor:
    """文本处理器

    提供链式调用的文本处理方法。

    Attributes:
        text: 当前文本内容
        history: 处理历史

    Example::

        processor = TextProcessor("Hello World")
        result = processor.lower().slugify().result
        # => "hello-world"
    """

    def __init__(self, text: str = ""):
        # TODO: 初始化 text 和 history
        pass

    @property
    def result(self) -> str:
        """获取当前处理结果"""
        return self.text

    def lower(self) -> "TextProcessor":
        """转小写

        Returns:
            self（支持链式调用）
        """
        # TODO: text 转小写，记录历史，返回 self
        pass

    def upper(self) -> "TextProcessor":
        """转大写"""
        # TODO: 同上
        pass

    def slugify(self, separator: str = "-") -> "TextProcessor":
        """转为 URL 友好的 slug 格式

        Args:
            separator: 分隔符（默认 "-"）

        Returns:
            self

        Example::

            TextProcessor("Hello World!").slugify()
            # text = "hello-world"
        """
        # TODO: 去特殊字符 -> 替换空格 -> 转小写
        pass

    def truncate(self, max_len: int = 50, suffix: str = "...") -> "TextProcessor":
        """截断文本

        Args:
            max_len: 最大长度
            suffix: 后缀
        """
        # TODO: 截断逻辑
        pass

    def replace(self, old: str, new: str) -> "TextProcessor":
        """替换文本"""
        # TODO: 封装 str.replace
        pass

    def get_history(self) -> list[str]:
        """获取处理历史

        Returns:
            所有执行过的操作名称列表
        """
        return self.history.copy()

    def __repr__(self) -> str:
        return f"TextProcessor({self.text!r})"


# ===== 文档工具函数 =====

def generate_api_docs(module_name: str, classes: dict, functions: dict) -> str:
    """生成简易 API 文档

    Args:
        module_name: 模块名
        classes: {类名: 类对象} 字典
        functions: {函数名: 函数对象} 字典

    Returns:
        Markdown 格式的 API 文档字符串
    """
    # TODO: 遍历 classes 和 functions，提取 docstring
    # 输出 Markdown 格式
    pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 包文档测试 ===")

    # 链式调用
    result = TextProcessor("Hello World!").lower().slugify().result
    print(f"slugify: {result}")

    # 截断
    result2 = TextProcessor("很长很长的文本" * 10).truncate(10).result
    print(f"truncate: {result2}")

    # 历史
    p = TextProcessor("test").lower().upper().slugify()
    print(f"历史: {p.get_history()}")

    # API 文档生成
    docs = generate_api_docs("string_utils", {"TextProcessor": TextProcessor}, {})
    print(f"\n--- API 文档 ---\n{docs[:200]}...")

    print("✅ Challenge 04 完成")
