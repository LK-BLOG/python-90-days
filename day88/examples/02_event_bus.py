# Day 88 示例 2: 事件系统
from typing import Dict, List, Callable, Any

class EventBus:
    def __init__(self): self.listeners: Dict[str, List[Callable]] = {}
    def on(self, event, callback):
        self.listeners.setdefault(event, []).append(callback)
    def emit(self, event, data=None):
        for cb in self.listeners.get(event, []): cb(data)
    def off(self, event, callback=None):
        if callback: self.listeners[event] = [c for c in self.listeners.get(event,[]) if c != callback]
        else: self.listeners.pop(event, None)

if __name__ == '__main__':
    bus = EventBus()
    bus.on('step', lambda d: print(f'  📊 步骤: {d}'))
    bus.on('error', lambda d: print(f'  ❌ 错误: {d}'))
    bus.emit('step', '完成第1步')
    bus.emit('step', '完成第2步')
    bus.emit('error', '超时')
