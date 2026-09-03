# -*- coding: utf-8 -*-
class RAGQuerier:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator
    def query(self, question, top_k=3):
        # TODO: 检索 + 生成
        pass
    def query_with_sources(self, question):
        # TODO: 返回答案+来源
        pass
