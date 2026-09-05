# -*- coding: utf-8 -*-
"""Day 68：离线评估RAG回答。"""
class EvalPractice:
    def evaluate_faithfulness(self, answer: str, context: str) -> float:
        """估计回答词语在上下文中的支持程度，返回0到1。"""
        if not answer.strip(): return 0.0
        # TODO：替换为句子级事实核验或模型评估
        words = set(answer.lower().split())
        supported = words & set(context.lower().split())
        return len(supported) / len(words) if words else 0.0
    def evaluate_relevancy(self, answer: str, question: str) -> float:
        """估计回答与问题的词汇相关性。"""
        if not answer.strip() or not question.strip(): return 0.0
        words = set(answer.lower().split())
        return len(words & set(question.lower().split())) / len(words)
if __name__ == "__main__": print(EvalPractice().evaluate_faithfulness("python guide", "python guide book"))
