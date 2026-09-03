# Day 81 示例 4: 上下文策略
class ContextStrategy:
    @staticmethod
    def sliding_window(messages: list, window: int = 10) -> list:
        return messages[-window:] if len(messages) > window else messages
    
    @staticmethod
    def summarize_old(messages: list) -> list:
        if len(messages) <= 10: return messages
        old, recent = messages[:-5], messages[-5:]
        return [{'role': 'system', 'content': f'摘要: 之前{len(old)}轮对话'}] + recent
    
    @staticmethod
    def keep_important(messages: list) -> list:
        return [m for m in messages if m.get('role') == 'user' or 'Tool:' in m.get('content', '')]

if __name__ == '__main__':
    msgs = [{'role': 'user', 'content': f'消息{i}'} for i in range(20)]
    print(f'滑动窗口: {len(ContextStrategy.sliding_window(msgs))} 条')
    print(f'摘要: {len(ContextStrategy.summarize_old(msgs))} 条')
    print(f'重要性: {len(ContextStrategy.keep_important(msgs))} 条')
