# -*- coding: utf-8 -*-
class TokenCounter:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
    def count(self, text):
        # TODO: 计算token数
        pass
    def estimate_cost(self, in_text, out_text):
        # TODO: 估算费用
        pass
if __name__ == "__main__":
    c = TokenCounter()
    print(f"Tokens: {c.count('你好世界')}")
