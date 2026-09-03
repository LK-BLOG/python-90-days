# -*- coding: utf-8 -*-
import re
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u4e00-\u9fff\w\s.,;:!?]', '', text)
    return text.strip()
def extract_metadata(text):
    return {"chars": len(text), "words": len(text.split()), "sentences": text.count('.') + text.count('!') + text.count('?')}
if __name__ == "__main__":
    print(clean_text("  Python  是   编程  语言  "))
    print(extract_metadata("Hello. World! Python?"))
