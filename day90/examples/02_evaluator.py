# Day 90 示例 2: 评估系统
import time

class RuntimeEvaluator:
    def __init__(self): self.evaluations = []
    def evaluate(self, goal, result, steps=0):
        metrics = {
            'has_result': bool(result) and len(result) > 5,
            'goal_met': goal.lower() in (result or '').lower(),
            'no_errors': '错误' not in (result or ''),
            'steps_executed': steps > 0,
        }
        score = sum(1 for v in metrics.values() if v) / len(metrics)
        eval_result = {'goal': goal, 'score': score, 'metrics': metrics, 'timestamp': time.time()}
        self.evaluations.append(eval_result)
        return eval_result
    def summary(self):
        if not self.evaluations: return {'total': 0}
        total = len(self.evaluations)
        avg = sum(e['score'] for e in self.evaluations) / total
        return {'total': total, 'avg_score': f'{avg:.2f}', 'success': f'{sum(1 for e in self.evaluations if e["score"]>=0.6)}/{total}'}

if __name__ == '__main__':
    ev = RuntimeEvaluator()
    print(ev.evaluate('测试任务', '测试结果: 完成'))
    print(ev.evaluate('搜索', '无结果'))
    print(f'汇总: {ev.summary()}')
