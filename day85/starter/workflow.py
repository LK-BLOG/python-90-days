# Day 85 骨架代码
class DAG:
    def __init__(self): pass
    def add_node(self, nid, name=''): pass
    def add_edge(self, fr, to): pass
    def topological_sort(self): pass

class WorkflowEngine:
    def __init__(self): pass
    def add_step(self, nid, name, handler): pass
    def add_edge(self, fr, to): pass
    def run(self): pass
