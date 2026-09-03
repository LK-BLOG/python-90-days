# -*- coding: utf-8 -*-
class DocumentPipeline:
    def __init__(self):
        self.loader = None
        self.chunker = None
        self.embedder = None
        self.store = None
    def setup(self, config=None):
        # TODO: 初始化管道
        pass
    def ingest(self, file_paths):
        # TODO: 加载 -> 分块 -> 嵌入 -> 存储
        pass
    def status(self):
        # TODO: 返回管道状态
        pass
