# -*- coding: utf-8 -*-
import numpy as np
import time

class FaissBuilder:
    def __init__(self, dim=8):
        self.dim = dim
        self.index = None
        self.build_time = 0
        self.search_time = 0
    
    def build_index(self, vectors, index_type="flat", nlist=10):
        # TODO: 根据类型构建FAISS索引
        # index_type: "flat", "ivf", "hnsw"
        pass
    
    def add_vectors(self, vectors):
        # TODO: 向索引中添加向量
        pass
    
    def search(self, query_vec, k=3):
        # TODO: 执行K近邻搜索
        pass
    
    def get_build_time(self):
        # TODO: 返回索引构建时间
        pass
    
    def get_search_time(self):
        # TODO: 返回上次搜索时间
        pass
