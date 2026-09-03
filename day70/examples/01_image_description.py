# -*- coding: utf-8 -*-
class ImageAnalyzer:
    def describe(self, path): return f"[模拟] {path}: 风景建筑"
    def ocr(self, path): return f"[OCR] {path}: Hello World"
if __name__ == "__main__":
    a = ImageAnalyzer()
    print(a.describe("photo.jpg"))
