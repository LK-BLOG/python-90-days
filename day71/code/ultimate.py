# -*- coding: utf-8 -*-
import json
class FinetuneDataset:
    def __init__(self, system_prompt=''):
        self.system = system_prompt
        self.conversations = []
    def add_qa(self, q, a):
        # TODO
        pass
    def validate_all(self):
        # TODO
        pass
    def export(self, path):
        # TODO
        pass
    def stats(self):
        # TODO
        pass
