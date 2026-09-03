# -*- coding: utf-8 -*-
class CostTracker:
    PRICING = {'gpt-4o': (2.5, 10.0), 'gpt-4o-mini': (0.15, 0.6)}
    def __init__(self):
        self.records = []
    def record(self, model, in_tok, out_tok):
        # TODO
        pass
    def total_cost(self):
        # TODO
        pass
    def by_model(self):
        # TODO
        pass
