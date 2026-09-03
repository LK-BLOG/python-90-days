# Day 80 - Example 2: System Prompt模板构建器

import re
from typing import Dict

class SystemPromptBuilder:
    """
    可参数化的System Prompt构建器
    支持:
    - 变量替换: 
    - 条件块: [[IF name]] ... [[ENDIF]]
    """

    def __init__(self, template: str):
        self.template = template
        self.variables: Dict[str, str] = {}
        self.conditionals: Dict[str, bool] = {}

    def set_var(self, key: str, value: str) -> 'SystemPromptBuilder':
        """设置模板变量"""
        self.variables[key] = value
        return self

    def set_conditional(self, name: str, enabled: bool) -> 'SystemPromptBuilder':
        """设置条件块开关"""
        self.conditionals[name] = enabled
        return self

    def build(self) -> str:
        """构建最终的System Prompt"""
        result = self.template
        # 替换变量
        for key, value in self.variables.items():
            placeholder = ""
            result = result.replace(placeholder, value)
        # 处理条件块
        for name, enabled in self.conditionals.items():
            pattern = r"\[\[IF " + re.escape(name) + r"\]\](.*?)\[\[ENDIF\]\]"
            if enabled:
                result = re.sub(pattern, r"\1", result, flags=re.DOTALL)
            else:
                result = re.sub(pattern, "", result, flags=re.DOTALL)
        # 清理多余空行
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip()

    def token_estimate(self) -> int:
        """估算构建后prompt的Token数"""
        return len(self.build()) // 3


if __name__ == "__main__":
    # 模板1: 通用助手
    template1 = """
# 角色
你是一个助手。

# 能力
- 
- 

# 约束
[[IF language_zh]]
请始终用中文回答。
[[ENDIF]]
[[IF verbose]]
请详细解释你的推理过程。
[[ENDIF]]
[[IF safety]]
不要生成有害或不当内容。
[[ENDIF]]
"""

    # 中文数据分析助手（简洁模式）
    builder1 = SystemPromptBuilder(template1)
    builder1.set_var("role", "数据分析")
    builder1.set_var("capability_1", "使用Python进行数据处理和可视化")
    builder1.set_var("capability_2", "编写SQL查询语句")
    builder1.set_conditional("language_zh", True)
    builder1.set_conditional("verbose", False)
    builder1.set_conditional("safety", True)

    prompt1 = builder1.build()
    print("=" * 60)
    print("助手配置1: 中文数据分析（简洁模式）")
    print("=" * 60)
    print(prompt1)
    print(f"\n估算Token数: {builder1.token_estimate()}")

    # 模板2: 代码审查助手
    template2 = """
# 角色
你是一个代码审查专家。

# 审查标准
1. 代码正确性
2. 性能优化
3. 安全漏洞
[[IF style_check]]
4. 代码风格和最佳实践
[[ENDIF]]
[[IF explain_fix]]
对于每个问题，请提供：
- 问题描述
- 风险等级 (低/中/高)
- 修复建议和代码示例
[[ENDIF]]
"""

    builder2 = SystemPromptBuilder(template2)
    builder2.set_var("language", "Python")
    builder2.set_conditional("style_check", True)
    builder2.set_conditional("explain_fix", True)

    prompt2 = builder2.build()
    print("\n" + "=" * 60)
    print("助手配置2: Python代码审查")
    print("=" * 60)
    print(prompt2)
    print(f"\n估算Token数: {builder2.token_estimate()}")
