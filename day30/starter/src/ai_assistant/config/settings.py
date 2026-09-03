"""Day 30 - 配置管理（pydantic-settings / dataclass）

支持环境变量、.env 文件，带类型验证。
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """应用配置

    优先级: 环境变量 > .env > 默认值
    """

    # API 配置
    api_key: str = ""
    model: str = "gpt-4"
    base_url: str = "https://api.openai.com/v1"
    temperature: float = 0.7
    max_tokens: int = 4096

    # Agent 配置
    max_iterations: int = 10
    system_prompt: str = "你是一个有用的 AI 助手。"

    # Memory 配置
    memory_type: str = "sliding_window"  # sliding_window / summary
    max_memory_tokens: int = 4000
    window_size: int = 20

    # 工具配置
    enable_tools: bool = True
    allowed_tool_dirs: list[str] = field(default_factory=lambda: ["."])

    # 日志配置
    log_level: str = "INFO"
    log_file: Optional[str] = None

    @classmethod
    def from_env(cls) -> Config:
        """从环境变量加载配置

        Returns:
            Config 实例
        """
        # TODO: 读取环境变量 AI_ASSISTANT_*
        # TODO: 读取 .env 文件
        # TODO: 返回合并后的 Config
        return cls(
            api_key=os.getenv("AI_ASSISTANT_API_KEY", ""),
            model=os.getenv("AI_ASSISTANT_MODEL", "gpt-4"),
        )

    @classmethod
    def from_dict(cls, data: dict) -> Config:
        """从字典创建配置

        Args:
            data: 配置字典

        Returns:
            Config 实例
        """
        # TODO: 过滤有效字段，创建 Config
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    def validate(self) -> list[str]:
        """验证配置项

        Returns:
            错误信息列表，空列表表示通过
        """
        errors = []
        if not self.api_key:
            errors.append("api_key 不能为空")
        if self.temperature < 0 or self.temperature > 2:
            errors.append("temperature 必须在 0-2 之间")
        if self.max_tokens < 1:
            errors.append("max_tokens 必须大于 0")
        if self.max_iterations < 1:
            errors.append("max_iterations 必须大于 0")
        return errors

    def to_dict(self) -> dict:
        """导出为字典"""
        from dataclasses import asdict
        return asdict(self)
