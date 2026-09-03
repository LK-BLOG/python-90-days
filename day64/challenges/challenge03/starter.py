# -*- coding: utf-8 -*-
class ToolCoordinator:
    def __init__(self):
        self.registry = {}
    def register(self, name, func):
        self.registry[name] = func
    def execute_calls(self, tool_calls):
        # TODO: 执行多个工具调用
        pass
