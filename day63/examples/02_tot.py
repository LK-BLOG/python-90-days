# -*- coding: utf-8 -*-
class TreeNode:
    def __init__(self, thought, parent=None):
        self.thought = thought
        self.children = []
        self.score = 0
    def add_child(self, thought):
        c = TreeNode(thought, self)
        self.children.append(c)
        return c

class TreeOfThoughts:
    def solve(self, problem):
        root = TreeNode(f"问题: {problem}")
        for t in ["方法1: 直接计算", "方法2: 分步推理", "方法3: 类比"]:
            c = root.add_child(t)
            c.score = hash(t) % 10
        best = max(root.children, key=lambda c: c.score)
        return {"best": best.thought, "all": [(c.thought, c.score) for c in root.children]}

if __name__ == "__main__":
    r = TreeOfThoughts().solve("如何优化Python性能?")
    print("最佳:", r["best"])
