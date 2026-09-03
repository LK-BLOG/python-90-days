# -*- coding: utf-8 -*-
import json
class ToolAssistant:
    def __init__(self):
        self.tools = {}
    def register_tool(self, name, func, desc):
        self.tools[name] = {"func": func, "desc": desc}
    def chat(self, user_input):
        tool_name = None
        for name in self.tools:
            if name in user_input.lower():
                tool_name = name
                break
        if tool_name:
            result = self.tools[tool_name]["func"]()
            return f"工具{tool_name}结果: {json.dumps(result, ensure_ascii=False)}"
        return f"收到: {user_input}"

if __name__ == "__main__":
    a = ToolAssistant()
    a.register_tool("time", lambda: {"time": "2024-01-01"}, "获取时间")
    print(a.chat("现在几点了?"))
    print(a.chat("你好"))
