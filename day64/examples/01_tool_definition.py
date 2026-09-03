# -*- coding: utf-8 -*-
import json
def define_tool(name, desc, params):
    return {"type": "function", "function": {"name": name, "description": desc, "parameters": params}}

WEATHER = define_tool("get_weather", "获取天气", {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]})
CALC = define_tool("calculate", "计算表达式", {"type": "object", "properties": {"expr": {"type": "string"}}, "required": ["expr"]})
SEARCH = define_tool("search", "搜索信息", {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})

if __name__ == "__main__":
    for t in [WEATHER, CALC, SEARCH]:
        print(f"{t['function']['name']}: {t['function']['description']}")
