# -*- coding: utf-8 -*-
class DocumentQA:
    def __init__(self):
        self.documents, self.index = [], {}
    def load_documents(self, docs):
        # TODO
        pass
    def answer(self, question, top_k=3):
        # TODO: 检索 + 生成
        pass
    def get_sources(self, question, top_k=3):
        # TODO: 返回引用来源
        pass
