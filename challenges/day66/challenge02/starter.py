# -*- coding: utf-8 -*-
import chromadb

class ChromaDocStore:
    def __init__(self, collection_name):
        # TODO: 初始化ChromaDB客户端和集合
        pass
    
    def add_documents(self, documents, metadatas=None, ids=None):
        # TODO: 批量添加文档
        pass
    
    def search(self, query, n_results=3):
        # TODO: 语义搜索相关文档
        pass
    
    def get_document(self, doc_id):
        # TODO: 根据ID获取文档
        pass
    
    def delete_documents(self, ids):
        # TODO: 删除指定ID的文档
        pass
