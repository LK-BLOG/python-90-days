# Day 81 示例 1: Token 计数器
class SimpleTokenCounter:
    def __init__(self):
        # 简化版：用字符数近似
        self.chars_per_token = 4
    
    def count(self, text: str) -> int:
        return len(text) // self.chars_per_token
    
    def count_messages(self, messages: list) -> int:
        return sum(self.count(m.get('content','')) for m in messages) + len(messages) * 4
    
    def fit_to_budget(self, messages: list, budget: int) -> list:
        if len(messages) <= 2: return messages
        system, query = messages[0], messages[-1]
        history = messages[1:-1]
        used = self.count_messages([system, query]) + 100
        kept = []
        for msg in reversed(history):
            t = self.count_messages([msg])
            if used + t > budget: break
            kept.insert(0, msg)
            used += t
        return [system] + kept + [query]

if __name__ == '__main__':
    tc = SimpleTokenCounter()
    msgs = [
        {'role': 'system', 'content': '你是助手'},
        {'role': 'user', 'content': '你好'},
        {'role': 'assistant', 'content': '你好！有什么帮助？'},
    ] * 20
    print(f'原始: {len(msgs)} 条, {tc.count_messages(msgs)} tokens')
    fitted = tc.fit_to_budget(msgs, 500)
    print(f'裁剪后: {len(fitted)} 条')
