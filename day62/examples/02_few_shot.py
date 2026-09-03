# -*- coding: utf-8 -*-
# Few-shot 分类
class FewShotClassifier:
    def __init__(self):
        self.examples = []
    def add_example(self, text, label):
        self.examples.append({"text": text, "label": label})
    def build_prompt(self, query):
        prompt = "分类示例:\n"
        for ex in self.examples:
            prompt += f'"{ex["text"]}" -> {ex["label"]}\n'
        prompt += f'\n"{query}" -> '
        return prompt
    def classify_simple(self, text):
        best, best_s = "未知", 0
        chars = set(text)
        for ex in self.examples:
            s = len(chars & set(ex["text"]))
            if s > best_s: best_s, best = s, ex["label"]
        return best

if __name__ == "__main__":
    clf = FewShotClassifier()
    clf.add_example("非常棒", "正面")
    clf.add_example("质量差", "负面")
    clf.add_example("还行", "中性")
    print(clf.build_prompt("好用"))
    print(f"分类: {clf.classify_simple('好用')}")
