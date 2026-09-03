# Challenge 1 Starter
# 实现 Config 类和项目骨架

# TODO:
# 1. 用 dataclass 或 dict 实现 Config
# 2. 支持 from_env() 和 from_file()
# 3. 实现 validate()
# 4. 在 __main__.py 中使用 Config

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """配置管理"""
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
        # TODO: 从环境变量读取
        ...

    def validate(self) -> list[str]:
        # TODO: 验证必要字段
        ...


if __name__ == "__main__":
    config = Config.from_env()
    errors = config.validate()
    if errors:
        print(f"配置错误: {errors}")
    else:
        print(f"配置OK: model={config.model}")
