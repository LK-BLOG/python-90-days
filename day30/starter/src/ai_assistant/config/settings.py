# 配置管理
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    api_key: str = ""
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    max_iterations: int = 10
    system_prompt: str = "你是一个有用的AI助手。"
    memory_max_tokens: int = 4000
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Config:
        # TODO: 从环境变量加载
        ...

    @classmethod
    def from_file(cls, path: str | Path = ".env") -> Config:
        # TODO: 从文件加载
        ...

    def validate(self) -> list[str]:
        # TODO: 验证配置
        ...
