# -*- coding: utf-8 -*-
import numpy as np
def simple_embedding(text, dim=8):
    vec = np.zeros(dim)
    for i, c in enumerate(text):
        vec[i % dim] += ord(c)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def cosine_sim(a, b):
    return float(np.dot(a, b))

if __name__ == "__main__":
    texts = ["Python编程", "机器学习", "天气预报"]
    vecs = [simple_embedding(t) for t in texts]
    q = simple_embedding("Python语言")
    for t, v in zip(texts, vecs):
        print(f"{t}: {cosine_sim(q, v):.4f}")
