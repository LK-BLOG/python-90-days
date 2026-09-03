# -*- coding: utf-8 -*-
import numpy as np
from typing import List, Dict

class EmbedGenerator:
    def __init__(self, dim=8):
        self.dim = dim
    
    def char_embedding(self, text: str) -> np.ndarray:
        # TODO: 基于字符的简单嵌入
        pass
    
    def bag_of_words_embedding(self, text: str, vocab: List[str] = None) -> np.ndarray:
        # TODO: 词袋模型嵌入
        pass
    
    def tfidf_embedding(self, text: str, vocab: List[str] = None, idf: Dict[str, float] = None) -> np.ndarray:
        # TODO: TF-IDF加权嵌入
        pass
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        # TODO: 计算余弦相似度
        pass
    
    def normalize(self, vec: np.ndarray) -> np.ndarray:
        # TODO: 向量归一化
        pass
