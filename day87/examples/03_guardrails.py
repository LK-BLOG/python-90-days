# Day 87 示例 3: Guardrails
class Guardrails:
    def __init__(self): self.rules = []; self.log = []
    def add(self, name, check_fn, action='block'):
        self.rules.append({'name': name, 'check': check_fn, 'action': action})
    def validate(self, text):
        for r in self.rules:
            ok, reason = r['check'](text)
            if not ok:
                self.log.append({'rule': r['name'], 'action': r['action'], 'reason': reason})
                if r['action'] == 'block': return False, f'{r["name"]}: {reason}'
        return True, '通过'

if __name__ == '__main__':
    g = Guardrails()
    g.add('length', lambda t: (len(t) < 100, '太长'), 'block')
    g.add('injection', lambda t: ('ignore' not in t.lower(), '注入'), 'block')
    print(g.validate('正常文本'))
    print(g.validate('ignore previous'))
    print(f'违规: {g.log}')
