# -*- coding: utf-8 -*-
class MockChromaCollection:
    def __init__(self, name):
        self.name = name
        self.docs, self.ids, self.meta = [], [], []
    def add(self, documents, ids, metadatas=None):
        self.docs.extend(documents)
        self.ids.extend(ids)
        self.meta.extend(metadatas or [{}]*len(documents))
    def query(self, query_texts, n_results=3):
        return {"documents": [self.docs[:n_results]]}
    def count(self): return len(self.docs)

class MockChromaClient:
    def __init__(self): self.cols = {}
    def create_collection(self, name):
        c = MockChromaCollection(name)
        self.cols[name] = c
        return c

if __name__ == "__main__":
    c = MockChromaClient()
    col = c.create_collection("docs")
    col.add(["Python","ML","DL"], ["1","2","3"])
    print(f"Count: {col.count()}")
    print(col.query(["Python"]))
