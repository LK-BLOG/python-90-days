# -*- coding: utf-8 -*-
import time, hashlib, json
class LLMClient:
    def __init__(self, default_model="gpt-4o-mini", max_retries=3, cache_enabled=True):
        self.default_model = default_model
        self.max_retries = max_retries
        self.cache_enabled = cache_enabled
        self._cache = {}
        self.stats = {"calls":0, "tokens":0, "cache_hits":0}
    def chat(self, messages_or_str, model=None, **kw):
        # TODO
        pass
    def stream(self, messages_or_str, model=None, **kw):
        # TODO
        pass
    def clear_cache(self):
        self._cache.clear()
