# -*- coding: utf-8 -*-
import time
class RateLimiter:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_time = time.time()
    def allow(self):
        # TODO: 令牌桶逻辑
        pass
