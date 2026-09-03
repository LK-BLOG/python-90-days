# -*- coding: utf-8 -*-
import re
class PromptTemplate:
    def __init__(self, template_str, defaults=None):
        self.template_str = template_str
        self.defaults = defaults or {}
        self.variables = re.findall(r'\{(\w+)\}', template_str)
    def render(self, **kwargs):
        # TODO: 合并defaults，检查变量，替换
        pass
