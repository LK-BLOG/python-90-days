# -*- coding: utf-8 -*-
"""Day 68：检索结果重排序。"""
from typing import Any
class RerankPractice:
    def rerank(self, query: str, results: list[dict[str, Any]], top_k: int = 3) -> list[dict[str, Any]]:
        """根据查询词覆盖率和原始分数重新排序。"""
        if top_k <= 0: raise ValueError("top_k必须大于0")
        words = set(query.lower().split())
        # TODO：替换为交叉编码器或其它reranker
        scored = []
        for item in results:
            text = str(item.get("text", ""))
            overlap = len(words & set(text.lower().split()))
            scored.append({**item, "rerank_score": overlap})
        return sorted(scored, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
if __name__ == "__main__": print(RerankPractice().rerank("python", [{"text":"python guide"}]))
