# -*- coding: utf-8 -*-
import numpy as np
def simple_emb(text, dim=8):
    vec = np.zeros(dim)
    for i, c in enumerate(text): vec[i % dim] += ord(c)
    n = np.linalg.norm(vec)
    return vec / n if n > 0 else vec

def cosine(a, b): return float(np.dot(a, b))

class SimpleRAG:
    def __init__(self, docs, chunk_size=200):
        self.chunks, self.vectors = [], []
        for doc in docs:
            for i in range(0, len(doc), chunk_size):
                c = doc[i:i+chunk_size]
                self.chunks.append(c)
                self.vectors.append(simple_emb(c))
    def retrieve(self, query, top_k=3):
        qv = simple_emb(query)
        sims = [(i, cosine(qv, v)) for i, v in enumerate(self.vectors)]
        sims.sort(key=lambda x: -x[1])
        return [(self.chunks[i], s) for i, s in sims[:top_k]]
    def answer(self, query):
        results = self.retrieve(query)
        ctx = "\n---\n".join(d for d, _ in results)
        return f"基于信息回答'{query}':\n{ctx}\n[此处调用LLM]"

if __name__ == "__main__":
    docs = ["Python是解释型语言，由Guido于1991年创建。", "机器学习是AI的分支，从数据中学习。", "深度学习用多层神经网络。"]
    print(SimpleRAG(docs).answer("Python是什么?"))
