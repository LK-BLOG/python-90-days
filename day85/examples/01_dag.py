# Day 85 示例 1: DAG 实现
from dataclasses import dataclass, field
from typing import Dict, List
from collections import defaultdict

class DAG:
    def __init__(self):
        self.nodes: Dict[str, dict] = {}
        self.edges: Dict[str, List[str]] = defaultdict(list)
        self.reverse: Dict[str, List[str]] = defaultdict(list)
    
    def add_node(self, nid, name=''):
        self.nodes[nid] = {'id': nid, 'name': name or nid}
    
    def add_edge(self, fr, to):
        self.edges[fr].append(to)
        self.reverse[to].append(fr)
    
    def topological_sort(self) -> list:
        in_deg = {n: len(self.reverse[n]) for n in self.nodes}
        q = [n for n,d in in_deg.items() if d == 0]
        result = []
        while q:
            n = q.pop(0); result.append(n)
            for nb in self.edges.get(n, []):
                in_deg[nb] -= 1
                if in_deg[nb] == 0: q.append(nb)
        if len(result) != len(self.nodes): raise ValueError('存在循环!')
        return result

if __name__ == '__main__':
    g = DAG()
    g.add_node('a', '搜索'); g.add_node('b', '分析'); g.add_node('c', '写报告')
    g.add_edge('a', 'b'); g.add_edge('b', 'c')
    print(f'拓扑排序: {g.topological_sort()}')
    print(f'有效: {g.validate() if hasattr(g,"validate") else "N/A"}')
