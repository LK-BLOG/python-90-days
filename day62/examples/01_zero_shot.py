# -*- coding: utf-8 -*-
# Zero-shot 分类
def zero_shot_classify(text, categories):
    keywords = {"正面":["好","棒","喜欢","满意"], "负面":["差","烂","失望","垃圾"], "中性":["一般","还行","普通"]}
    scores = {cat: sum(1 for kw in keywords.get(cat,[]) if kw in text) for cat in categories}
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "未知"

if __name__ == "__main__":
    for t in ["太好用了!", "服务太差了", "还行吧"]:
        print(f"{t} -> {zero_shot_classify(t, ['正面','负面','中性'])}")
