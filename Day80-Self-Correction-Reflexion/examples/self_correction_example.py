'''
Day 80 示例：自我纠正系统
'''

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from datetime import datetime
import asyncio


class ErrorType(Enum):
    '''错误类型'''
    TOOL_ERROR = "tool_error"
    LOGIC_ERROR = "logic_error"
    INPUT_ERROR = "input_error"
    TIMEOUT_ERROR = "timeout_error"


@dataclass
class ExecutionError:
    '''执行错误'''
    error_type: ErrorType
    message: str
    step_id: str | None = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ErrorDetector:
    '''错误检测器'''
    
    def detect(self, result: Any, step: Any) -> ExecutionError | None:
        '''检测错误'''
        if result is None:
            return ExecutionError(ErrorType.LOGIC_ERROR, "结果为空")
        
        if isinstance(result, Exception):
            error_type = ErrorType.TOOL_ERROR
            if "timeout" in str(result).lower():
                error_type = ErrorType.TIMEOUT_ERROR
            return ExecutionError(error_type, str(result))
        
        if hasattr(result, 'success') and not result.success:
            return ExecutionError(
                ErrorType.TOOL_ERROR,
                getattr(result, 'error', '未知错误')
            )
        
        return None


class SelfCorrector:
    '''自我纠正器'''
    
    def correct(self, error: ExecutionError, context: dict) -> dict:
        '''生成纠正方案'''
        if error.error_type == ErrorType.TIMEOUT_ERROR:
            return {"action": "retry", "reason": "超时重试"}
        elif error.error_type == ErrorType.TOOL_ERROR:
            return {"action": "use_different_tool", "reason": "换工具"}
        elif error.error_type == ErrorType.INPUT_ERROR:
            return {"action": "fix_input", "reason": "修正输入"}
        else:
            return {"action": "rethink", "reason": "重新思考"}


class ReflexionAgent:
    '''反思Agent'''
    
    def __init__(self):
        self.episodes: list[dict] = []
    
    def reflect(self, task: str, action: str, result: str) -> str:
        '''进行反思'''
        reflection = self._generate_reflection(task, action, result)
        
        self.episodes.append({
            "task": task,
            "action": action,
            "result": result,
            "reflection": reflection,
            "timestamp": datetime.now()
        })
        
        return reflection
    
    def _generate_reflection(self, task: str, action: str, result: str) -> str:
        '''生成反思'''
        if "成功" in result:
            return "执行成功，可以继续当前方法"
        else:
            return "需要调整方法"


def main():
    '''演示自我纠正'''
    print("=" * 60)
    print("自我纠正系统演示")
    print("=" * 60)
    
    detector = ErrorDetector()
    corrector = SelfCorrector()
    reflexion = ReflexionAgent()
    
    # 模拟执行
    class MockResult:
        def __init__(self, success: bool, error: str = None):
            self.success = success
            self.error = error
    
    # 测试正常情况
    print("\n1. 正常执行:")
    result = MockResult(True, None)
    error = detector.detect(result, None)
    print(f"   错误检测: {error}")
    
    # 测试错误情况
    print("\n2. 错误执行:")
    result = MockResult(False, "工具执行失败")
    error = detector.detect(result, None)
    print(f"   错误检测: {error.message}")
    
    correction = corrector.correct(error, {"task": "test"})
    print(f"   纠正方案: {correction}")
    
    # 反思
    print("\n3. 反思:")
    reflection = reflexion.reflect("测试任务", "执行", "部分成功")
    print(f"   反思结果: {reflection}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
