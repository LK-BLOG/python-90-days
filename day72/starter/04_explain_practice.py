# -*- coding: utf-8 -*-
"""Day 72：安全地生成可审计的解释信息。"""
class ExplainPractice:
    def explain(self, input_text: str, output: str) -> dict[str, object]:
        """返回决策摘要、证据和风险，不暴露隐藏思维链。"""
        # TODO：使用简短理由和可验证证据，不保存内部隐式推理
        return {"input":input_text,"output":output,"reason_summary":"待补充","evidence":[],"risks":[]}
    def extract_steps(self, cot_text: str) -> list[str]:
        """从公开的步骤文本提取编号步骤；过滤敏感内容。"""
        # TODO：限制长度，清除凭据和系统提示
        return [line.strip() for line in cot_text.splitlines() if line.strip()]
if __name__ == "__main__": print(ExplainPractice().extract_steps("1. 检索
2. 验证"))
