# Day 81 骨架代码
class TokenCounter:
    def __init__(self):
        self.chars_per_token = 4
    def count(self, text: str) -> int:
        # TODO: 计算 token 数
        pass
    def fit_to_budget(self, messages: list, budget: int) -> list:
        # TODO: 裁剪到预算内
        pass

class ContextCompressor:
    def compress(self, messages: list, max_messages: int = 10) -> list:
        # TODO: 压缩消息
        pass

class DynamicPromptBuilder:
    def add(self, name: str, content: str, priority: int = 0):
        pass
    def build(self, budget: int = 4000) -> str:
        # TODO: 构建 prompt
        pass
