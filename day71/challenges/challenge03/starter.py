# -*- coding: utf-8 -*-
class FinetuneConfig:
    def __init__(self):
        self.params = {'n_epochs': 3, 'batch_size': 1, 'learning_rate_multiplier': 1.8}
    def validate(self):
        # TODO
        pass
    def estimate_cost(self, data_size):
        # TODO
        pass
