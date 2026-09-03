# -*- coding: utf-8 -*-
class RAGPipeline:
    def __init__(self, chunk_size=200):
        self.chunk_size = chunk_size
    def ingest(self, documents):
        # TODO: 分块 + 向量化 + 存储
        pass
    def retrieve(self, query, top_k=3):
        # TODO
        pass
    def generate_prompt(self, query, retrieved):
        # TODO: 构建prompt
        pass
