# -*- coding: utf-8 -*-
"""Day 67：文档文本清洗与规范化。"""
import re

class CleanPractice:
    """清除噪声，同时保留对检索有价值的文本。"""
    def clean(self, text: str) -> str:
        """去除HTML标签、链接、控制字符和多余空白。"""
        if not isinstance(text, str): raise TypeError("text必须是字符串")
        # TODO：按课程要求补充HTML、URL和特殊字符规则
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"https?://\S+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def normalize(self, text: str) -> str:
        """统一大小写、标点间空格和换行格式。"""
        # TODO：考虑中英文混排和保留代码块的策略
        return self.clean(text).lower()

if __name__ == "__main__":
    print(CleanPractice().normalize("<p>Hello</p>  Python"))
