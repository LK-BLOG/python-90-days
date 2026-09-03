# -*- coding: utf-8 -*-
import numpy as np

class VectorApp:
    def __init__(self, dim=8):
        self.dim = dim
        self.documents = []  # 所有文档片段
        self.vectors = []    # 对应向量
        self.history = []    # 搜索历史
    
    def load_document(self, filepath, chunk_size=100):
        # TODO: 导入文档并分块
        pass
    
    def search(self, query, top_k=5, method="semantic"):
        # TODO: 搜索文档
        # method: "semantic" 或 "keyword"
        pass
    
    def show_history(self):
        # TODO: 显示搜索历史
        pass
    
    def get_stats(self):
        # TODO: 返回系统统计信息
        pass
    
    def clear_history(self):
        # TODO: 清空搜索历史
        pass
