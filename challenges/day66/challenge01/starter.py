# -*- coding: utf-8 -*-
import numpy as np

class VectorDB:
    def __init__(self, dim=8):
        self.dim = dim
        self.vectors = {}  # id -> vector
        self.metadata = {}  # id -> metadata
    
    def insert(self, id, vector, meta=None):
        # TODO: 插入向量和元数据
        pass
    
    def delete(self, id):
        # TODO: 删除指定ID的向量
        pass
    
    def cosine_similarity(self, a, b):
        # TODO: 计算两个向量的余弦相似度
        pass
    
    def search(self, query_vec, top_k=3):
        # TODO: 返回最相似的top_k个向量
        pass
