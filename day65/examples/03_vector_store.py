# -*- coding: utf-8 -*-
import numpy as np
class SimpleVectorStore:
    def __init__(self):
        self.vectors = []
        self.documents = []
    def add(self, doc, vec):
        self.documents.append(doc)
        self.vectors.append(np.array(vec))
    def search(self, query_vec, top_k=3):
        q = np.array(query_vec)
        sims = [(i, float(np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v)))) for i, v in enumerate(self.vectors)]
        sims.sort(key=lambda x: -x[1])
        return [(self.documents[i], score) for i, score in sims[:top_k]]
    def __len__(self):
        return len(self.documents)

if __name__ == "__main__":
    store = SimpleVectorStore()
    for doc, vec in zip(["Python教程","ML入门","深度学习"], [[1,0,0],[0,1,0],[0,0,1]]):
        store.add(doc, vec)
    for doc, score in store.search([0.9,0.1,0], 2):
        print(f"{doc}: {score:.4f}")
