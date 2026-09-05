# -*- coding: utf-8 -*-
"""Day 72：基于证据的幻觉检测骨架。"""
class HallucinationPractice:
    def check(self, answer: str, context: str) -> dict[str, object]:
        """检查回答中的声明是否能在上下文中找到证据。"""
        if not answer.strip(): raise ValueError("回答不能为空")
        # TODO：按句拆分声明，进行NLI/引用级核验
        words=set(answer.lower().split()); evidence=set(context.lower().split())
        ratio=len(words & evidence)/len(words) if words else 0.0
        return {"supported": ratio >= 0.6, "score": ratio, "unsupported_terms": sorted(words-evidence)}
    def confidence(self, answer: str, context: str) -> float:
        """返回0到1之间的证据支持置信度。"""
        return float(self.check(answer, context)["score"])
if __name__ == "__main__": print(HallucinationPractice().check("python", "python guide"))
