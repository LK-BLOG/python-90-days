# -*- coding: utf-8 -*-
"""Day 67：关键词+语义分数的混合检索。"""
from typing import Any

class HybridPractice:
    """合并关键词匹配分和向量相似度分。"""
    def search(self, query: str, docs: list[dict[str, Any]], top_k: int = 3) -> list[dict[str, Any]]:
        """按 alpha * semantic + (1-alpha) * keyword 排序。"""
        if top_k <= 0: raise ValueError("top_k必须大于0")
        # TODO：实现关键词分、语义分归一化和加权融合
        ranked = []
        for doc in docs:
            text = str(doc.get("text", ""))
            score = sum(1 for word in query.lower().split() if word in text.lower())
            ranked.append({**doc, "keyword_score": score})
        return sorted(ranked, key=lambda x: x["keyword_score"], reverse=True)[:top_k]

if __name__ == "__main__":
    print(HybridPractice().search("python", [{"text":"learn python"}]))
