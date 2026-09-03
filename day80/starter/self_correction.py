# Day 80 骨架代码
from dataclasses import dataclass, field
from typing import List

class ReflexionAgent:
    def __init__(self, max_retries=3):
        # TODO: 初始化
        pass
    
    def run(self, goal: str) -> str:
        # TODO: 带反思的执行循环
        pass
    
    def _execute_with_context(self, goal: str) -> str:
        # TODO: 带反思上下文执行
        pass
    
    def _evaluate(self, result: str, goal: str) -> tuple:
        # TODO: 评估结果
        pass
    
    def _reflect(self, goal: str, result: str, evaluation: str) -> str:
        # TODO: 生成反思
        pass

class StateManager:
    def __init__(self):
        # TODO: 初始化
        pass
    def save(self, name=''):
        pass
    def rollback(self):
        pass
