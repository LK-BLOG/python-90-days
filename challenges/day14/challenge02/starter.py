"""Challenge 2: MRO 分析器"""
class A:
    def process(self): return ['A']

class B(A):
    def process(self): return super().process() + ['B']

class C(A):
    def process(self): return super().process() + ['C']

class D(B, C):
    def process(self): return super().process() + ['D']

# TODO: 打印 D 的 MRO
# TODO: 分析 D().process() 的输出
d = D()
print(d.process())
