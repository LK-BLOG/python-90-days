# Day 80 示例 4: 回滚机制
import copy, time

class StateManager:
    def __init__(self):
        self.state = {}
        self.history = []
    
    def save(self, name=''):
        self.history.append({'name': name, 'state': copy.deepcopy(self.state), 'time': time.time()})
    
    def update(self, key, value):
        self.state[key] = value
    
    def rollback(self):
        if not self.history: return False
        snapshot = self.history.pop()
        self.state = copy.deepcopy(snapshot['state'])
        return True
    
    def get(self):
        return dict(self.state)

if __name__ == '__main__':
    sm = StateManager()
    sm.save('初始')
    sm.update('x', 1)
    sm.save('第一次更新')
    sm.update('x', 2)
    print(f'当前: {sm.get()}')
    sm.rollback()
    print(f'回滚后: {sm.get()}')
