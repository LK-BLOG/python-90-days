# -*- coding: utf-8 -*-
class ContentFilter:
    def __init__(self):
        self.blocked = []
        self.warning = []
    def add_rule(self, pattern, level='block'):
        # TODO
        pass
    def check(self, text):
        # TODO
        pass
    def filter(self, text):
        # TODO: 过滤并返回安全文本
        pass
