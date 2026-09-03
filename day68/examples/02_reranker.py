# -*- coding: utf-8 -*-
class SimpleReranker:
    def rerank(self, query, results, top_k=3):
        scored = []
        for doc, score in results:
            boost = 0.2 if any(w in doc.lower() for w in query.lower().split()) else 0
            scored.append((doc, score + boost))
        scored.sort(key=lambda x: -x[1])
        return scored[:top_k]
if __name__ == "__main__":
    r = SimpleReranker()
    print(r.rerank("Python", [("Java教程",0.5),("Python入门",0.4),("Python高级",0.3)]))
