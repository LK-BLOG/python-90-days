"""Day 30 - Prompt 模板管理"""
from __future__ import annotations


class PromptTemplate:
    """Prompt 模板管理器"""

    DEFAULT_SYSTEM = """你是一个有用的 AI 助手。你可以使用工具来完成用户的任务。
当需要使用工具时，请调用相应的工具函数。"""

    CODE_REVIEW_SYSTEM = """你是一个专业的代码审查机器人。
请按以下格式返回审查结果：
- 问题列表（含行号、严重程度、描述、建议）
- 总体评分（0-100）"""

    def __init__(self, template: str = ""):
        """初始化

        Args:
            template: 模板字符串，支持 {variable} 占位符
        """
        self.template = template or self.DEFAULT_SYSTEM

    def format(self, **kwargs) -> str:
        """格式化模板

        Args:
            **kwargs: 模板变量

        Returns:
            格式化后的字符串
        """
        # TODO: 替换模板中的 {variable} 占位符
        ...

    @classmethod
    def truncate(cls, text: str, max_tokens: int = 3000) -> str:
        """截断过长的文本

        Args:
            text: 原始文本
            max_tokens: 最大 token 数

        Returns:
            截断后的文本
        """
        # TODO: 按行保留前 N 行，添加截断提示
        lines = text.split("\n")
        # 粗略估算：每行约 20 token
        estimated_lines = max_tokens // 20
        if len(lines) > estimated_lines:
            return "\n".join(lines[:estimated_lines]) + f"\n\n... (已截断，共 {len(lines)} 行)"
        return text
