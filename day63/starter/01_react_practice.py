# -*- coding: utf-8 -*-
# ReAct练习
class ReActPractice:
    def __init__(self):
        self.tools = {}
    def register(self, name, func):
        self.tools[name] = func
    def think(self, thought):
        print(f"思考: {thought}")
    def act(self, tool_call):
        # TODO: 解析并执行
        pass
