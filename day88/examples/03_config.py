# Day 88 示例 3: 配置管理
from dataclasses import dataclass, field
from typing import List

@dataclass
class RuntimeConfig:
    model: str = 'gpt-4'
    max_steps: int = 20
    temperature: float = 0.7
    enabled_tools: List[str] = field(default_factory=lambda: ['calculator', 'search'])
    cost_limit: float = 10.0
    enable_tracing: bool = True
    
    @classmethod
    def from_dict(cls, data): return cls(**{k:v for k,v in data.items() if k in cls.__dataclass_fields__})

if __name__ == '__main__':
    config = RuntimeConfig()
    print(f'模型: {config.model}, 步数: {config.max_steps}')
    custom = RuntimeConfig.from_dict({'model': 'gpt-3.5', 'max_steps': 5})
    print(f'自定义: {custom.model}, 步数: {custom.max_steps}')
