# Day 86 示例 3: 成本追踪
class CostTracker:
    PRICES = {'gpt-4': {'in': 0.03, 'out': 0.06}, 'gpt-3.5': {'in': 0.001, 'out': 0.002}}
    def __init__(self): self.records = []; self.total_cost = 0
    def record(self, model, in_tok, out_tok):
        p = self.PRICES.get(model, {'in': 0.01, 'out': 0.02})
        cost = (in_tok * p['in'] + out_tok * p['out']) / 1000
        self.records.append({'model': model, 'tokens': in_tok+out_tok, 'cost': cost})
        self.total_cost += cost; return cost
    def summary(self):
        return {'calls': len(self.records), 'total_cost': f''}

if __name__ == '__main__':
    ct = CostTracker()
    ct.record('gpt-4', 500, 200); ct.record('gpt-3.5', 1000, 500)
    print(f'成本: {ct.summary()}')
