"""Day 30 示例：Config模块参考实现"""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """配置管理 — 环境变量 > 配置文件 > 默认值"""
    
    # API配置
    api_key: str = ""
    model: str = "gpt-4o-mini"
    base_url: str | None = None
    
    # 生成参数
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Agent配置
    max_iterations: int = 10
    system_prompt: str = "你是一个有用的AI助手。可以使用工具来帮助用户完成任务。"
    
    # Memory配置
    memory_max_tokens: int = 4000
    memory_max_messages: int = 50
    
    # 工具配置
    enable_tools: list[str] | None = None  # None = 全部启用
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str | None = None
    
    @classmethod
    def from_env(cls) -> Config:
        """从环境变量加载"""
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("AI_ASSISTANT_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("AI_ASSISTANT_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("AI_ASSISTANT_MAX_TOKENS", "2000")),
            max_iterations=int(os.getenv("AI_ASSISTANT_MAX_ITERATIONS", "10")),
            log_level=os.getenv("AI_ASSISTANT_LOG_LEVEL", "INFO"),
        )
    
    @classmethod
    def from_file(cls, path: str | Path = ".env") -> Config:
        """从.env文件加载"""
        config = cls.from_env()
        env_path = Path(path)
        
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    if key == "OPENAI_API_KEY":
                        config.api_key = value
                    elif key == "AI_ASSISTANT_MODEL":
                        config.model = value
        
        return config
    
    def validate(self) -> list[str]:
        """验证配置，返回错误列表"""
        errors = []
        if not self.api_key:
            errors.append("未设置 OPENAI_API_KEY")
        if self.temperature < 0 or self.temperature > 2:
            errors.append(f"temperature 必须在 0-2 之间，当前: {self.temperature}")
        if self.max_tokens < 1:
            errors.append(f"max_tokens 必须大于 0，当前: {self.max_tokens}")
        return errors


if __name__ == "__main__":
    config = Config.from_env()
    errors = config.validate()
    if errors:
        print("配置错误:", errors)
    else:
        print(f"配置加载成功: model={config.model}, temp={config.temperature}")
