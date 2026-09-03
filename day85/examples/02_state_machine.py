# Day 85 示例 2: 状态机
from collections import defaultdict

class StateMachine:
    def __init__(self):
        self.transitions = []
        self.current = ''
        self.history = []
    
    def add_transition(self, fr, to, condition=''):
        self.transitions.append({'from': fr, 'to': to, 'cond': condition})
    
    def start(self, state):
        self.current = state; self.history = [state]
    
    def transition(self, to):
        valid = any(t['from'] == self.current and t['to'] == to for t in self.transitions)
        if not valid: return False
        self.current = to; self.history.append(to); return True

if __name__ == '__main__':
    sm = StateMachine()
    sm.add_transition('idle', 'planning')
    sm.add_transition('planning', 'executing')
    sm.add_transition('executing', 'done')
    sm.start('idle')
    print(f'当前: {sm.current}')
    sm.transition('planning'); print(f'转移到: {sm.current}')
    sm.transition('executing'); print(f'转移到: {sm.current}')
    print(f'历史: {sm.history}')
