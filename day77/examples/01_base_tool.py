# Day 77 示例 1: BaseTool 实现
\"\"\"
工具抽象基类的完整实现
\"\"\"
from abc import ABC, abstractmethod
from typing import Any, Type
from dataclasses import dataclass, field
import traceback


@dataclass
class ToolResult:
    \"\"\"工具执行结果\"\"\"
    success: bool
    data: Any = None
    error: str = ""
    metadata: dict = field(default_factory=dict)
    
    def __repr__(self):
        if self.success:
            return f"ToolResult(success, data={self.data!r})"
        return f"ToolResult(failed, error='{self.error}')"


class BaseTool(ABC):
    \"\"\"工具抽象基类\"\"\"
    
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    category: str = "general"
    
    def to_dict(self) -> dict:
        \"\"\"序列化为字典\"\"\"
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
        }
    
    def validate_params(self, params: dict) -> dict:
        \"\"\"参数验证（子类可重写）\"\"\"
        return params
    
    def run(self, **kwargs) -> ToolResult:
        \"\"\"安全执行（带错误处理）\"\"\"
        try:
            validated = self.validate_params(kwargs)
            result = self.execute(**validated)
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(
                success=False, 
                error=f"{type(e).__name__}: {e}",
                metadata={"traceback": traceback.format_exc()}
            )
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        \"\"\"实际执行逻辑\"\"\"
        pass


# 具体工具实现
class CalculatorTool(BaseTool):
    name = "calculator"
    description = "执行安全的数学计算"
    category = "math"
    
    ALLOWED_NAMES = {"abs": abs, "round": round, "min": min, "max": max, "sum": sum}
    
    def validate_params(self, params: dict) -> dict:
        if "expression" not in params:
            raise ValueError("缺少参数 'expression'")
        return params
    
    def execute(self, expression: str) -> str:
        # 安全计算
        result = eval(expression, {"__builtins__": {}}, self.ALLOWED_NAMES)
        return str(result)


class UpperCaseTool(BaseTool):
    name = "uppercase"
    description = "将文本转为大写"
    category = "text"
    
    def execute(self, text: str) -> str:
        return text.upper()


# 测试
if __name__ == "__main__":
    calc = CalculatorTool()
    upper = UpperCaseTool()
    
    # 正常执行
    print("计算 2+3*4:", calc.run(expression="2+3*4"))
    print("转大写:", upper.run(text="hello world"))
    
    # 错误处理
    print("缺少参数:", calc.run())
    print("非法表达式:", calc.run(expression="import os"))
