# -*- coding: utf-8 -*-
import time
class RateLimitPractice:
    def __init__(self, rate, cap):
        self.rate, self.cap = rate, cap
        self.tokens, self.last = cap, time.time()
    def allow(self):
        # TODO
        pass
