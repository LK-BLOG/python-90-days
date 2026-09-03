# -*- coding: utf-8 -*-
class PDFParser:
    def extract_text(self, path): return f"[模拟] {path} 文本..."
    def extract_pages(self, path): return [f"第{i+1}页" for i in range(3)]
if __name__ == "__main__":
    print(PDFParser().extract_text("doc.pdf"))
