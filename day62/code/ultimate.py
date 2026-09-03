# -*- coding: utf-8 -*-
import re, json
from datetime import datetime
class PromptTemplate:
    def __init__(self, name, template_str, system_prompt=None):
        self.name = name
        self.template_str = template_str
        self.variables = re.findall(r'\{(\w+)\}', template_str)
        self.system_prompt = system_prompt
        self.version = 1
    def render(self, **kwargs):
        # TODO
        pass
    def update(self, new_template):
        # TODO
        pass
class TemplateLibrary:
    def __init__(self):
        self.templates = {}
    def add(self, template):
        # TODO
        pass
    def get(self, name):
        # TODO
        pass
    def search(self, keyword):
        # TODO
        pass
    def list_all(self):
        # TODO
        pass
