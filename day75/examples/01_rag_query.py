# -*- coding: utf-8 -*-
class RAGQuerier:
    def __init__(self, retriever): self.retriever = retriever
    def query(self, question, top_k=3):
        results = self.retriever.search(question, top_k)
        ctx = "\n".join(r[0] if isinstance(r,tuple) else r for r in results)
        return f"基于信息回答'{question}':\n{ctx}"
if __name__ == "__main__":
    class Mock:
        def search(self,q,k): return [("文档1",0.9),("文档2",0.8)]
    print(RAGQuerier(Mock()).query("Python是什么?"))
