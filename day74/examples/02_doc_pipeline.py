# -*- coding: utf-8 -*-
class DocumentPipeline:
    def __init__(self): self.docs, self.chunks = [], []
    def load(self, path):
        self.docs.append({"path":path,"text":f"[加载] {path}"})
    def chunk(self, text, size=200):
        return [text[i:i+size] for i in range(0,len(text),size)]
    def process(self, paths):
        for p in paths:
            self.load(p)
            self.chunks.extend(self.chunk(self.docs[-1]["text"]))
        return self.chunks
if __name__ == "__main__":
    p = DocumentPipeline()
    print(f"Chunks: {len(p.process(['a.pdf','b.docx']))}")
