# Day 85 示例 3: 工作流引擎
from collections import defaultdict

class WorkflowEngine:
    def __init__(self):
        self.nodes = {}; self.edges = defaultdict(list); self.reverse = defaultdict(list)
        self.results = {}
    
    def add_step(self, nid, name, handler):
        self.nodes[nid] = {'name': name, 'handler': handler}
    
    def add_edge(self, fr, to):
        self.edges[fr].append(to); self.reverse[to].append(fr)
    
    def run(self):
        roots = [n for n in self.nodes if not self.reverse[n]]
        for r in roots: self._execute(r)
        return self.results
    
    def _execute(self, nid):
        if nid in self.results: return
        for dep in self.reverse.get(nid, []):
            if dep not in self.results: self._execute(dep)
        node = self.nodes[nid]
        deps_results = {d: self.results.get(d) for d in self.reverse.get(nid, [])}
        result = node['handler'](**deps_results) if deps_results else node['handler']()
        self.results[nid] = result
        print(f'  ✅ {node["name"]}: {result}')
        for nb in self.edges.get(nid, []): self._execute(nb)

if __name__ == '__main__':
    we = WorkflowEngine()
    we.add_step('a', '搜索', lambda: '搜索结果')
    we.add_step('b', '分析', lambda a: f'分析: {a}')
    we.add_step('c', '写报告', lambda b: f'报告: {b}')
    we.add_edge('a', 'b'); we.add_edge('b', 'c')
    print('=== 工作流执行 ===')
    we.run()
