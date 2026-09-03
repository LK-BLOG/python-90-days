# -*- coding: utf-8 -*-
class IndexBuilder:
    def __init__(self):
        self.chunks = []
        self.vectors = []
    def add_document(self, doc, chunker):
        # TODO: 分块 + 嵌入 + 存储
        pass
    def build_index(self):
        # TODO: 构建搜索索引
        pass
    def search(self, query, top_k=5):
        # TODO
        pass
