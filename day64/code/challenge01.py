# -*- coding: utf-8 -*-
class ToolRegistry:
    def __init__(self):
        self.tools = {}
    def register(self, name, func, desc, params):
        # TODO
        pass
    def get_definitions(self):
        # TODO: 返回JSON Schema定义
        pass
    def execute(self, name, **kw):
        # TODO
        pass
