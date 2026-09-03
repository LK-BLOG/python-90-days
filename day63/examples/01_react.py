# -*- coding: utf-8 -*-
import re
class ReActAgent:
    def __init__(self):
        self.tools = {}
        self.trace = []
    def register_tool(self, name, func):
        self.tools[name] = func
    def think(self, thought):
        self.trace.append(f"思考: {thought}")
    def act(self, action_str):
        m = re.match(r'(\w+)\((.*)\)', action_str)
        if not m: return f"无法解析: {action_str}"
        name, args = m.group(1), m.group(2)
        if name not in self.tools: return f"未知工具: {name}"
        result = self.tools[name](args)
        self.trace.append(f"行动: {action_str}")
        self.trace.append(f"观察: {result}")
        return result
    def get_trace(self):
        return "\n".join(self.trace)

if __name__ == "__main__":
    agent = ReActAgent()
    agent.register_tool("calc", lambda x: eval(x))
    agent.think("需要计算 3*5+2")
    agent.act("calc(3*5+2)")
    print(agent.get_trace())
