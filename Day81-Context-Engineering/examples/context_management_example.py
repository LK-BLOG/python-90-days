'''
Day 81 示例：上下文管理
'''

import tiktoken
from dataclasses import dataclass
from typing import Any


class ContextManager:
    '''上下文管理器'''
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        '''计算token数'''
        return len(self.encoder.encode(text))
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        '''截断到指定token数'''
        tokens = self.encoder.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoder.decode(tokens[:max_tokens]) + "..."
    
    def build_context(self, parts: list[dict]) -> str:
        '''构建上下文'''
        result = []
        remaining = self.max_tokens
        
        for part in parts:
            text = part.get("content", "")
            priority = part.get("priority", 0)
            tokens = self.count_tokens(text)
            
            # 高优先级的内容优先保留
            if tokens <= remaining:
                result.append(text)
                remaining -= tokens
            elif priority > 0:
                # 高优先级，截断保留
                truncated = self.truncate_to_tokens(text, remaining)
                result.append(truncated)
                break
            else:
                continue
        
        return "\n\n".join(result)


class ContextCompressor:
    '''上下文压缩器'''
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        '''生成摘要'''
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    def extract_key_points(self, text: str, max_points: int = 3) -> list[str]:
        '''提取关键点'''
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        return sentences[:max_points]


def main():
    '''演示上下文管理'''
    print("=" * 60)
    print("上下文管理演示")
    print("=" * 60)
    
    manager = ContextManager(max_tokens=100)
    compressor = ContextCompressor()
    
    # 测试token计数
    text = "这是一个测试文本，用于演示上下文管理功能。"
    tokens = manager.count_tokens(text)
    print(f"\n文本: {text}")
    print(f"Token数: {tokens}")
    
    # 测试截断
    long_text = "这是" * 50
    truncated = manager.truncate_to_tokens(long_text, 20)
    print(f"\n截断后的文本: {truncated}")
    
    # 测试上下文构建
    parts = [
        {"content": "系统提示：你是一个助手。", "priority": 10},
        {"content": "用户问题：什么是Python？", "priority": 5},
        {"content": "历史对话摘要..." * 20, "priority": 1}
    ]
    
    context = manager.build_context(parts)
    print(f"\n构建的上下文:\n{context}")
    
    # 测试压缩
    long_content = "这是关于Python的介绍。Python是一种流行的编程语言。它简单易学。" * 5
    summary = compressor.summarize(long_content, 50)
    print(f"\n摘要: {summary}")
    
    key_points = compressor.extract_key_points(long_content)
    print(f"\n关键点: {key_points}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
