# Day 81 示例 3: 动态 Prompt 构建器
class DynamicPromptBuilder:
    def __init__(self):
        self.sections = {}
        self.base = '你是一个智能助手。'
    
    def add(self, name: str, content: str, priority: int = 0):
        self.sections[name] = {'content': content, 'priority': priority}
    
    def build(self, budget: int = 4000) -> str:
        sorted_sections = sorted(self.sections.items(), key=lambda x: x[1]['priority'], reverse=True)
        prompt = self.base
        used = len(prompt) // 4
        for name, info in sorted_sections:
            text = f'\n\n## {name}\n{info["content"]}'
            tokens = len(text) // 4
            if used + tokens < budget - 200:
                prompt += text
                used += tokens
            else:
                remaining = (budget - used - 200) * 4
                if remaining > 100:
                    prompt += f'\n\n## {name} (部分)\n{info["content"][:remaining]}...'
                break
        return prompt

if __name__ == '__main__':
    dp = DynamicPromptBuilder()
    dp.add('角色', '你是一个Python专家', priority=10)
    dp.add('工具', '可用工具: search, calculator, code_exec', priority=8)
    dp.add('约束', '回答要简洁', priority=5)
    prompt = dp.build(budget=500)
    print(prompt)
