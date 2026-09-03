# Day 80: Self-Correction & 反思

## 1. 为什么 Agent 需要反思？

大多数 LLM Agent 会犯错。没有反思机制的 Agent 会：
- 在同一个错误上反复失败
- 无法从失败中学习
- 生成低质量的输出

反思让 Agent 能够：
1. **检测错误**：识别自己的输出是否有问题
2. **纠正错误**：自动修复或换个方法
3. **学习经验**：避免重复犯错

## 2. Reflexion 模式

### 2.1 核心思想

Reflexion 让 Agent 在失败后：
1. 分析失败原因
2. 生成反思（类似经验总结）
3. 将反思加入上下文
4. 重新尝试

`python
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Attempt:
    \"\"\"一次尝试\"\"\"
    step: int
    action: str
    result: str
    success: bool
    reflection: str = ""


class ReflexionAgent:
    \"\"\"带反思能力的 Agent\"\"\"
    
    def __init__(self, max_retries: int = 3, max_reflections: int = 3):
        self.max_retries = max_retries
        self.max_reflections = max_reflections
        self.attempts: List[Attempt] = []
        self.reflections: List[str] = []
    
    def run(self, goal: str) -> str:
        \"\"\"带反思的执行循环\"\"\"
        for attempt_num in range(self.max_retries):
            print(f"\n=== 尝试 {attempt_num + 1} ===")
            
            # 1. 执行（带上之前的反思）
            result = self._execute_with_context(goal)
            
            # 2. 评估结果
            success, evaluation = self._evaluate(result, goal)
            
            if success:
                print(f"✅ 成功! 结果: {result}")
                return result
            
            # 3. 反思失败原因
            print(f"❌ 失败: {evaluation}")
            reflection = self._reflect(goal, result, evaluation)
            self.reflections.append(reflection)
            print(f"💭 反思: {reflection}")
            
            # 4. 记录尝试
            self.attempts.append(Attempt(
                step=attempt_num + 1,
                action=f"尝试完成: {goal}",
                result=result,
                success=False,
                reflection=reflection
            ))
        
        return f"经过 {self.max_retries} 次尝试后仍然失败"
    
    def _execute_with_context(self, goal: str) -> str:
        \"\"\"执行时加入历史反思\"\"\"
        context = f"目标: {goal}"
        if self.reflections:
            context += "\n\n之前的经验教训:\n"
            for i, r in enumerate(self.reflections):
                context += f"  {i+1}. {r}\n"
        
        # 模拟 LLM 执行（实际中调用 LLM）
        return f"基于目标 '{goal}' 的执行结果"
    
    def _evaluate(self, result: str, goal: str) -> tuple[bool, str]:
        \"\"\"评估结果质量\"\"\"
        # 简单评估（实际中用 LLM 评估）
        if "错误" in result or "失败" in result:
            return False, "结果包含错误标记"
        if len(result) < 10:
            return False, "结果太短，可能不完整"
        return True, "评估通过"
    
    def _reflect(self, goal: str, result: str, evaluation: str) -> str:
        \"\"\"生成反思（模拟 LLM）\"\"\"
        # 实际中让 LLM 分析失败原因
        return f"目标 '{goal}' 未能完成，原因: {evaluation}。下次应该..."
`

## 3. 自我纠正循环

`python
class SelfCorrectionLoop:
    \"\"\"自我纠正循环\"\"\"
    
    def __init__(self, llm, tools: dict, max_corrections: int = 3):
        self.llm = llm
        self.tools = tools
        self.max_corrections = max_corrections
    
    def run(self, task: str) -> str:
        \"\"\"执行并自我纠正\"\"\"
        # 第一次执行
        output = self._generate(task)
        
        for correction_round in range(self.max_corrections):
            # 检查输出
            issues = self._check_output(output, task)
            
            if not issues:
                print(f"✅ 第 {correction_round + 1} 轮检查通过")
                return output
            
            print(f"⚠️ 发现 {len(issues)} 个问题:")
            for issue in issues:
                print(f"  - {issue}")
            
            # 纠正
            output = self._correct(output, issues, task)
        
        return output
    
    def _generate(self, task: str) -> str:
        \"\"\"生成初始输出\"\"\"
        # 模拟 LLM 生成
        return f"初始输出: {task}"
    
    def _check_output(self, output: str, task: str) -> list:
        \"\"\"检查输出问题\"\"\"
        issues = []
        
        # 示例检查规则
        if "TODO" in output:
            issues.append("输出中包含未完成的 TODO")
        if len(output) < 50:
            issues.append("输出太简短，可能不完整")
        if "错误" in output:
            issues.append("输出包含错误信息")
        if output.count("\n") < 3:
            issues.append("输出格式不够丰富")
        
        return issues
    
    def _correct(self, output: str, issues: list, task: str) -> str:
        \"\"\"根据问题纠正输出\"\"\"
        # 模拟 LLM 纠正
        correction_prompt = f"""原始输出:
{output}

发现的问题:
{chr(10).join(f'- {i}' for i in issues)}

请修正这些问题，生成更好的输出。"""
        
        return f"修正后的输出: {task} (已修正 {len(issues)} 个问题)"
`

## 4. 重试策略

`python
import time
from functools import wraps
from typing import Callable, Any


class RetryStrategy:
    \"\"\"重试策略\"\"\"
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        \"\"\"带重试的执行\"\"\"
        last_error = None
        current_delay = self.delay
        
        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                last_error = e
                print(f"  ⚠️ 尝试 {attempt + 1} 失败: {e}")
                
                if attempt < self.max_retries - 1:
                    print(f"  ⏳ 等待 {current_delay:.1f}s 后重试...")
                    time.sleep(current_delay)
                    current_delay *= self.backoff
        
        raise last_error


# 装饰器版本
def retry(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator

# 使用
@retry(max_retries=3, delay=0.5)
def unreliable_api_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("API 调用失败")
    return "成功!"
`

## 5. 回滚机制

`python
from typing import Optional


class StateManager:
    \"\"\"状态管理器 - 支持回滚\"\"\"
    
    def __init__(self):
        self.state = {}
        self.history: List[dict] = []
        self.current_version = 0
    
    def save(self, name: str = ""):
        \"\"\"保存当前状态\"\"\"
        import copy
        snapshot = copy.deepcopy(self.state)
        self.history.append({
            "version": self.current_version,
            "name": name,
            "state": snapshot,
            "timestamp": time.time()
        })
        self.current_version += 1
    
    def update(self, key: str, value: Any):
        \"\"\"更新状态\"\"\"
        self.state[key] = value
    
    def rollback(self, version: int = None) -> bool:
        \"\"\"回滚到指定版本\"\"\"
        if not self.history:
            return False
        
        if version is None:
            # 回滚到上一个版本
            snapshot = self.history.pop()
        else:
            # 回滚到指定版本
            for i, h in enumerate(self.history):
                if h["version"] == version:
                    snapshot = self.history.pop(i)
                    break
            else:
                return False
        
        self.state = copy.deepcopy(snapshot["state"])
        return True
    
    def get_state(self) -> dict:
        return dict(self.state)
`

## 6. 常见错误

1. **反思太浅**：只说"失败了"而不分析原因 → 要求 LLM 给出具体原因和改进方案
2. **无限反思**：反思后还是同样的结果 → 设置最大反思次数
3. **没有记忆**：不把反思结果加入上下文 → 维护反思历史列表
4. **忽略成本**：每次反思都是一次 LLM 调用 → 设置反思预算

## 7. 动手练习

### 练习 1：实现 Reflexion 循环
### 练习 2：实现自我纠正检查器
### 练习 3：实现带回滚的状态管理
