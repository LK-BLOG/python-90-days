# -*- coding: utf-8 -*-
import time
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate, self.capacity = rate, capacity
        self.tokens, self.last = capacity, time.time()
    def allow(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
if __name__ == "__main__":
    b = TokenBucket(2, 5)
    for i in range(8):
        print(f"Req {i+1}: {'OK' if b.allow() else 'BLOCKED'}")
        time.sleep(0.3)
