# -*- coding: utf-8 -*-
"""Day 68：HyDE——先生成假设文档，再进行检索。"""
from typing import Callable, Any
class HyDEPractice:
    def generate_hypothesis(self, question: str) -> str:
        """生成与问题相关的假设性答案文本。"""
        if not question.strip(): raise ValueError("问题不能为空")
        # TODO：接入LLM或离线模板生成假设文档
        return "假设文档：" + question.strip()
    def retrieve(self, question: str, retriever: Callable[[str], list[Any]]) -> list[Any]:
        """使用假设文档作为查询调用检索器。"""
        hypothesis = self.generate_hypothesis(question)
        return retriever(hypothesis)
if __name__ == "__main__": print(HyDEPractice().generate_hypothesis("什么是RAG？"))
