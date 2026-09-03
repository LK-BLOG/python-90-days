# Day 86 示例 2: Trace 系统
import time, uuid

class Tracer:
    def __init__(self):
        self.spans = []; self.current = None; self.trace_id = str(uuid.uuid4())[:8]
    def start(self, name):
        span = {'id': str(uuid.uuid4())[:6], 'name': name, 'start': time.time(), 'status': 'ok'}
        self.spans.append(span); self.current = span; return span
    def end(self, status='ok'):
        if self.current: self.current['end'] = time.time(); self.current['status'] = status; self.current = None
    def get_duration(self, span):
        return (span.get('end', time.time()) - span['start']) * 1000
    def print_trace(self):
        for s in self.spans:
            d = self.get_duration(s)
            icon = '✅' if s['status'] == 'ok' else '❌'
            print(f'  {icon} {s["name"]}: {d:.1f}ms')

if __name__ == '__main__':
    t = Tracer()
    s1 = t.start('agent_step'); time.sleep(0.05); t.end()
    s2 = t.start('tool_call'); time.sleep(0.03); t.end()
    print(f'Trace {t.trace_id}:'); t.print_trace()
