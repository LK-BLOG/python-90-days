# -*- coding: utf-8 -*-
import numpy as np
class SimpleFAISS:
    def __init__(self, dim):
        self.dim = dim
        self.vecs, self.ids = [], []
    def add(self, vectors, ids):
        for v, id in zip(vectors, ids):
            self.vecs.append(np.array(v))
            self.ids.append(id)
    def search(self, query, k=3):
        q = np.array(query)
        sims = [(i, float(np.dot(q,v)/(np.linalg.norm(q)*np.linalg.norm(v)))) for i,v in enumerate(self.vecs)]
        sims.sort(key=lambda x: -x[1])
        return [(self.ids[i],s) for i,s in sims[:k]]

if __name__ == "__main__":
    idx = SimpleFAISS(3)
    idx.add([[1,0,0],[0,1,0],[0,0,1]], ["d1","d2","d3"])
    print(idx.search([0.9,0.1,0]))
