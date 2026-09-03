# Day 81 示例 2: 上下文压缩器
class ContextCompressor:
    def compress(self, messages: list, max_messages: int = 10) -> list:
        if len(messages) <= max_messages: return messages
        old, recent = messages[:-5], messages[-5:]
        topics = set()
        for m in old:
            c = m.get('content', '')
            for kw in ['搜索', '代码', '分析', '文件', '数据']:
                if kw in c: topics.add(kw)
        summary = f'之前{len(old)}轮讨论了: {", ".join(topics)}' if topics else f'之前{len(old)}轮对话'
        return [{'role': 'system', 'content': summary}] + recent

if __name__ == '__main__':
    cc = ContextCompressor()
    msgs = [{'role': 'user', 'content': f'消息{i} 搜索数据'} for i in range(20)]
    compressed = cc.compress(msgs)
    print(f'压缩: {len(msgs)} → {len(compressed)} 条')
    print(f'摘要: {compressed[0]["content"]}')
