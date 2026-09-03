# -*- coding: utf-8 -*-
def rewrite_query(original):
    synonyms = {"Python":"Python编程", "AI":"人工智能", "ML":"机器学习"}
    expanded = original
    for k,v in synonyms.items():
        if k.lower() in original.lower():
            expanded += f" ({v})"
    return expanded
if __name__ == "__main__":
    print(rewrite_query("Python AI 教程"))
