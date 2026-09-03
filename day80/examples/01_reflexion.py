# Day 80 示例 1: Reflexion Agent
from dataclasses import dataclass, field
from typing import List

@dataclass
class Attempt:
    step: int; action: str; result: str; success: bool; reflection: str = ''

class ReflexionAgent:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.attempts: List[Attempt] = []
        self.reflections: List[str] = []
    
    def run(self, goal: str) -> str:
        for i in range(self.max_retries):
            print(f'\n=== 尝试 {i+1} ===')
            # 带反思执行
            context = f'目标: {goal}'
            if self.reflections:
                context += '\n历史教训:\n' + '\n'.join(f'  - {r}' for r in self.reflections)
            
            # 模拟执行
            result = f'执行结果: {goal}'
            success = '错误' not in result and len(result) > 10
            
            if success:
                self.attempts.append(Attempt(i+1, goal, result, True))
                print(f'✅ 成功!')
                return result
            
            # 反思
            reflection = f'尝试{i+1}失败，需要改进方法'
            self.reflections.append(reflection)
            self.attempts.append(Attempt(i+1, goal, result, False, reflection))
            print(f'💭 反思: {reflection}')
        
        return '多次尝试后仍失败'

if __name__ == '__main__':
    agent = ReflexionAgent(max_retries=3)
    print(agent.run('写一个排序算法'))
