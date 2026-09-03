# -*- coding: utf-8 -*-
import asyncio
class AsyncLLMCaller:
    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    async def call(self, messages, model='gpt-4o-mini'):
        # TODO: 限流异步调用
        pass
    async def batch_call(self, batch):
        # TODO: 并发调用多条
        pass
