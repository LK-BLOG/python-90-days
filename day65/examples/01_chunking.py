# -*- coding: utf-8 -*-
def fixed_chunks(text, size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

def sentence_chunks(text, max_chunk=500):
    sentences = text.replace(".", ".\n").split("\n")
    chunks, cur = [], ""
    for s in sentences:
        s = s.strip()
        if not s: continue
        if len(cur) + len(s) > max_chunk and cur:
            chunks.append(cur.strip())
            cur = s
        else:
            cur += s
    if cur.strip(): chunks.append(cur.strip())
    return chunks

if __name__ == "__main__":
    doc = "Python是解释型语言。支持多种范式。语法简洁。广泛用于Web和AI。"
    for i, c in enumerate(fixed_chunks(doc, 20, 5)):
        print(f"块{i+1}: {c}")
