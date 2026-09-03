# -*- coding: utf-8 -*-
import asyncio
class AsyncPractice:
    def __init__(self, max_concurrent=5):
        self.sem = asyncio.Semaphore(max_concurrent)
    async def call(self, messages):
        # TODO
        pass
