# Day 80 Challenge 2: System Prompt模板系统 ⭐⭐
# 构建一个可参数化的System Prompt模板系统

"""
实现一个SystemPromptBuilder，支持：
1. 变量替换 ()
2. 条件块 ([[IF name]] ... [[ENDIF]])
3. Prompt版本管理（保存/加载不同版本）
4. Token估算

类设计:
- SystemPromptBuilder: 模板构建
- PromptRegistry: 版本管理
"""

class SystemPromptBuilder:
    def __init__(self, template: str):
        pass

    def set_var(self, key: str, value: str) -> 'SystemPromptBuilder':
        pass

    def set_conditional(self, name: str, enabled: bool) -> 'SystemPromptBuilder':
        pass

    def build(self) -> str:
        pass

    def estimate_tokens(self) -> int:
        pass


class PromptRegistry:
    """Prompt版本管理"""
    def __init__(self):
        self.prompts = {}

    def register(self, name: str, builder: SystemPromptBuilder):
        pass

    def get(self, name: str) -> str:
        pass

    def list_versions(self) -> list:
        pass


if __name__ == "__main__":
    builder = SystemPromptBuilder("你是。[[IF zh]]请用中文回答。[[ENDIF]]")
    builder.set_var("role", "助手").set_conditional("zh", True)
    print(builder.build())
