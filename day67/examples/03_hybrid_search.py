# -*- coding: utf-8 -*-
def keyword_search(query, docs, top_k=3):
    words = set(query.lower().split())
    scored = [(i, len(words & set(d.lower().split()))/max(len(words),1)) for i,d in enumerate(docs)]
    scored.sort(key=lambda x: -x[1])
    return [(docs[i],s) for i,s in scored[:top_k]]
if __name__ == "__main__":
    docs = ["Python教程","ML入门","Python数据分析"]
    print(keyword_search("Python", docs))
