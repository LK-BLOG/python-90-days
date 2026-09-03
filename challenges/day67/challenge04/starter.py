# -*- coding: utf-8 -*-
import numpy as np
from typing import List, Dict, Tuple
from collections import Counter
import math

class HybridSearch:
    def __init__(self, documents: List[str]):
        self.documents = documents
        self.doc_vectors = []
        self.inverted_index = {}  # word -> [doc_indices]
        self.doc_freqs = {}       # word -> document frequency
    
    def vector_search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        # TODO: 向量搜索
        pass
    
    def bm25_search(self, query: str, top_k: int = 5, k1: float = 1.5, b: float = 0.75) -> List[Tuple[int, float]]:
        # TODO: BM25关键词搜索
        pass
    
    def hybrid_search(self, query: str, top_k: int = 5, vector_weight: float = 0.7) -> List[Tuple[int, float, str]]:
        # TODO: 混合搜索（向量+关键词）
        pass
    
    def build_inverted_index(self):
        # TODO: 构建倒排索引
        pass
    
    def compute_idf(self, word: str) -> float:
        # TODO: 计算IDF
        pass
