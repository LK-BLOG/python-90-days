# -*- coding: utf-8 -*-
import numpy as np

class MultiVectorDB:
    def __init__(self, dim=8):
        self.dim = dim
        self.collections = {}  # name -> {vectors: {}, metadata: {}}
    
    def create_collection(self, name):
        # TODO: 创建新集合
        pass
    
    def delete_collection(self, name):
        # TODO: 删除集合
        pass
    
    def list_collections(self):
        # TODO: 列出所有集合
        pass
    
    def insert(self, collection, id, vector, meta=None):
        # TODO: 向指定集合插入向量
        pass
    
    def search(self, query_vec, collections=None, top_k=3):
        # TODO: 跨集合搜索
        pass
    
    def get_stats(self):
        # TODO: 返回每个集合的统计信息
        pass
