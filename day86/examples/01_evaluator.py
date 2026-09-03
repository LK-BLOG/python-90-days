# Day 86 示例 1: Agent 评估器
import time

class AgentEvaluator:
    def __init__(self): self.results = []
    
    def evaluate(self, task_id, output, expected='', duration=0, tokens=0):
        score = 0.5
        if expected and output.strip() == expected.strip(): score += 0.3
        if len(output) > 50: score += 0.1
        if duration < 10: score += 0.1
        score = min(score, 1.0)
        result = {'task_id': task_id, 'score': score, 'success': score >= 0.6, 'duration': duration}
        self.results.append(result)
        return result
    
    def summary(self):
        if not self.results: return {}
        return {'total': len(self.results), 'avg_score': sum(r['score'] for r in self.results)/len(self.results)}

if __name__ == '__main__':
    ev = AgentEvaluator()
    print(ev.evaluate('t1', '结果A', '结果A', 2.5, 100))
    print(ev.evaluate('t2', '结果B', '结果C', 5.0, 200))
    print(f'汇总: {ev.summary()}')
