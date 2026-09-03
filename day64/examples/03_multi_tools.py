# -*- coding: utf-8 -*-
import json
class ToolRegistry:
    def __init__(self):
        self._tools = {}
    def register(self, name, func, desc, params):
        self._tools[name] = {"func": func, "desc": desc, "params": params}
    def get_definitions(self):
        return [{"type": "function", "function": {"name": n, "description": t["desc"], "parameters": t["params"]}} for n, t in self._tools.items()]
    def execute(self, name, **kw):
        if name not in self._tools: return {"error": f"未知工具: {name}"}
        return self._tools[name]["func"](**kw)

if __name__ == "__main__":
    reg = ToolRegistry()
    from datetime import datetime
    reg.register("time", lambda: {"time": datetime.now().isoformat()}, "获取时间", {"type": "object", "properties": {}})
    reg.register("add", lambda a, b: {"result": a+b}, "加法", {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a","b"]})
    print(reg.execute("time"))
    print(reg.execute("add", a=3, b=5))
