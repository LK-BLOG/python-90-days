# -*- coding: utf-8 -*-
import json
class MockToolCaller:
    def __init__(self):
        self.tools = {}
    def register(self, name, func):
        self.tools[name] = func
    def handle(self, response):
        if "tool_calls" in response:
            results = []
            for call in response["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                result = self.tools[name](**args)
                results.append({"tool_call_id": call["id"], "content": json.dumps(result)})
            return results
        return [{"role": "assistant", "content": response.get("content", "")}]

if __name__ == "__main__":
    caller = MockToolCaller()
    caller.register("calc", lambda expr: {"result": eval(expr)})
    resp = {"tool_calls": [{"id": "c1", "function": {"name": "calc", "arguments": json.dumps({"expr": "3*5+2"})}}]}
    print(caller.handle(resp))
