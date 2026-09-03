# Day 80 课程：Self-Correction & 反思

## 1. 错误检测机制

`python
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from datetime import datetime


class ErrorType(Enum):
    '''错误类型'''
    TOOL_ERROR = "tool_error"
    LOGIC_ERROR = "logic_error"
    INPUT_ERROR = "input_error"
    TIMEOUT_ERROR = "timeout_error"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class ExecutionError:
    '''执行错误'''
    error_type: ErrorType
    message: str
    step_id: str | None = None
    tool_name: str | None = None
    timestamp: datetime = None
    context: dict | None = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ErrorDetector:
    '''错误检测器'''
    
    def detect(self, result: Any, step: Any) -> ExecutionError | None:
        '''检测错误'''
        if result is None:
            return ExecutionError(
                error_type=ErrorType.UNKNOWN_ERROR,
                message="结果为空",
                step_id=getattr(step, 'id', None)
            )
        
        if isinstance(result, Exception):
            return self._classify_exception(result, step)
        
        if hasattr(result, 'success') and not result.success:
            return ExecutionError(
                error_type=ErrorType.TOOL_ERROR,
                message=getattr(result, 'error', '未知错误'),
                step_id=getattr(step, 'id', None),
                tool_name=getattr(step, 'tool_name', None)
            )
        
        return None
    
    def _classify_exception(self, exc: Exception, step: Any) -> ExecutionError:
        '''分类异常'''
        error_type = ErrorType.UNKNOWN_ERROR
        
        if "timeout" in str(exc).lower():
            error_type = ErrorType.TIMEOUT_ERROR
        elif "tool" in str(exc).lower():
            error_type = ErrorType.TOOL_ERROR
        elif "input" in str(exc).lower() or "argument" in str(exc).lower():
            error_type = ErrorType.INPUT_ERROR
        
        return ExecutionError(
            error_type=error_type,
            message=str(exc),
            step_id=getattr(step, 'id', None)
        )
`

## 2. 自我纠正循环

`python
@dataclass
class CorrectionStrategy:
    '''纠正策略'''
    error_type: ErrorType
    max_retries: int = 3
    backoff_factor: float = 1.5
    fallback_action: Callable | None = None


class SelfCorrector:
    '''自我纠正器'''
    
    def __init__(self, llm_provider: Callable = None):
        self.llm_provider = llm_provider
        self.strategies: dict[ErrorType, CorrectionStrategy] = {}
        self.correction_history: list[dict] = []
    
    def register_strategy(self, error_type: ErrorType, strategy: CorrectionStrategy):
        '''注册纠正策略'''
        self.strategies[error_type] = strategy
    
    def should_retry(self, error: ExecutionError, attempt: int) -> bool:
        '''是否应该重试'''
        strategy = self.strategies.get(error.error_type)
        if not strategy:
            return False
        return attempt < strategy.max_retries
    
    def correct(self, error: ExecutionError, context: dict) -> dict:
        '''生成纠正方案'''
        prompt = self._build_correction_prompt(error, context)
        
        # 这里应该调用LLM，简化处理
        correction = self._generate_correction(error, context)
        
        # 记录纠正历史
        self.correction_history.append({
            "error": error,
            "correction": correction,
            "timestamp": datetime.now()
        })
        
        return correction
    
    def _build_correction_prompt(self, error: ExecutionError, context: dict) -> str:
        '''构建纠正提示'''
        return f\"\"\"
执行过程中出现错误，请分析并提供纠正方案：

错误类型: {error.error_type.value}
错误信息: {error.message}
步骤ID: {error.step_id}
工具名称: {error.tool_name}

上下文:
{context}

请提供:
1. 错误原因分析
2. 纠正方案
3. 预期结果
\"\"\"
    
    def _generate_correction(self, error: ExecutionError, context: dict) -> dict:
        '''生成纠正方案（模拟）'''
        if error.error_type == ErrorType.TIMEOUT_ERROR:
            return {
                "action": "retry_with_simplified_input",
                "reason": "执行超时，简化输入后重试"
            }
        elif error.error_type == ErrorType.TOOL_ERROR:
            return {
                "action": "try_different_tool",
                "reason": "工具执行失败，尝试使用其他工具"
            }
        elif error.error_type == ErrorType.INPUT_ERROR:
            return {
                "action": "fix_input_format",
                "reason": "输入格式错误，修正后重试"
            }
        else:
            return {
                "action": "rethink_approach",
                "reason": "未知错误，重新思考方法"
            }
`

## 3. 反思模式（Reflexion）

`python
@dataclass
class ReflexionEpisode:
    '''反思 episode'''
    task: str
    action: str
    result: str
    reflection: str
    score: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ReflexionAgent:
    '''Reflexion Agent'''
    
    def __init__(self, llm_provider: Callable = None):
        self.llm_provider = llm_provider
        self.episodes: list[ReflexionEpisode] = []
        self.memory: list[str] = []
    
    def reflect(self, task: str, action: str, result: str) -> str:
        '''进行反思'''
        # 构建反思提示
        prompt = self._build_reflection_prompt(task, action, result)
        
        # 生成反思（模拟）
        reflection = self._generate_reflection(task, action, result)
        
        # 记录episode
        episode = ReflexionEpisode(
            task=task,
            action=action,
            result=result,
            reflection=reflection,
            score=self._evaluate_result(result)
        )
        self.episodes.append(episode)
        
        # 更新记忆
        self.memory.append(f"任务: {task}, 结果: {result}, 反思: {reflection}")
        
        return reflection
    
    def get_similar_episodes(self, task: str, k: int = 3) -> list[ReflexionEpisode]:
        '''获取相似的历史episode'''
        # 简化的相似度计算
        scored_episodes = []
        for ep in self.episodes:
            score = self._similarity(task, ep.task)
            scored_episodes.append((score, ep))
        
        # 排序并返回top-k
        scored_episodes.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored_episodes[:k]]
    
    def _build_reflection_prompt(self, task: str, action: str, result: str) -> str:
        '''构建反思提示'''
        similar = self.get_similar_episodes(task)
        history = "\n".join([
            f"- 任务: {ep.task}, 反思: {ep.reflection}"
            for ep in similar
        ])
        
        return f\"\"\"
请对以下情况进行反思：

任务: {task}
执行的动作: {action}
执行结果: {result}

历史相似任务的反思:
{history}

请回答:
1. 这次做得好的地方
2. 需要改进的地方
3. 下次应该怎么做
\"\"\"
    
    def _generate_reflection(self, task: str, action: str, result: str) -> str:
        '''生成反思（模拟）'''
        if "成功" in result or "完成" in result:
            return "执行成功，可以继续当前方法"
        else:
            return "执行未达预期，需要调整方法"
    
    def _evaluate_result(self, result: str) -> float:
        '''评估结果'''
        if "成功" in result or "完成" in result:
            return 1.0
        elif "部分" in result:
            return 0.5
        else:
            return 0.0
    
    def _similarity(self, text1: str, text2: str) -> float:
        '''简单的相似度计算'''
        words1 = set(text1)
        words2 = set(text2)
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0
`

## 4. 重试策略与回滚

`python
from enum import Enum
import asyncio
import random


class RetryStrategy(Enum):
    '''重试策略'''
    FIXED = "fixed"           # 固定间隔
    EXPONENTIAL = "exponential"  # 指数退避
    LINEAR = "linear"         # 线性增长
    RANDOM = "random"         # 随机间隔


class RetryManager:
    '''重试管理器'''
    
    def __init__(
        self,
        max_retries: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        self.max_retries = max_retries
        self.strategy = strategy
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        '''带重试的执行'''
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                last_error = e
                
                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    print(f"重试 {attempt + 1}/{self.max_retries}，等待 {delay:.2f} 秒...")
                    await asyncio.sleep(delay)
        
        raise last_error
    
    def _calculate_delay(self, attempt: int) -> float:
        '''计算延迟时间'''
        if self.strategy == RetryStrategy.FIXED:
            return self.base_delay
        elif self.strategy == RetryStrategy.EXPONENTIAL:
            delay = self.base_delay * (2 ** attempt)
        elif self.strategy == RetryStrategy.LINEAR:
            delay = self.base_delay * (attempt + 1)
        elif self.strategy == RetryStrategy.RANDOM:
            delay = self.base_delay * random.uniform(1, 2 ** attempt)
        else:
            delay = self.base_delay
        
        return min(delay, self.max_delay)


class CheckpointManager:
    '''检查点管理器，支持回滚'''
    
    def __init__(self):
        self.checkpoints: list[dict] = []
    
    def save_checkpoint(self, state: dict, step_id: str):
        '''保存检查点'''
        self.checkpoints.append({
            "step_id": step_id,
            "state": state.copy(),
            "timestamp": datetime.now()
        })
        print(f"保存检查点: {step_id}")
    
    def rollback(self, step_id: str) -> dict | None:
        '''回滚到指定检查点'''
        for i in range(len(self.checkpoints) - 1, -1, -1):
            if self.checkpoints[i]["step_id"] == step_id:
                state = self.checkpoints[i]["state"]
                # 删除之后的检查点
                self.checkpoints = self.checkpoints[:i + 1]
                print(f"回滚到检查点: {step_id}")
                return state
        return None
    
    def get_latest_checkpoint(self) -> dict | None:
        '''获取最新检查点'''
        if self.checkpoints:
            return self.checkpoints[-1]
        return None
`

## 5. 完整的自我纠正Agent

`python
class SelfCorrectingAgent:
    '''带自我纠正能力的Agent'''
    
    def __init__(self, llm_provider: Callable = None):
        self.llm_provider = llm_provider
        self.error_detector = ErrorDetector()
        self.self_corrector = SelfCorrector(llm_provider)
        self.retry_manager = RetryManager(max_retries=3)
        self.checkpoint_manager = CheckpointManager()
        self.reflexion = ReflexionAgent(llm_provider)
    
    async def execute_with_correction(
        self,
        task: str,
        executor: Callable,
        *args,
        **kwargs
    ) -> Any:
        '''带自我纠正的执行'''
        # 保存初始检查点
        self.checkpoint_manager.save_checkpoint(
            {"task": task, "status": "started"},
            "initial"
        )
        
        attempt = 0
        max_attempts = 5
        
        while attempt < max_attempts:
            try:
                # 执行任务
                result = await executor(task, *args, **kwargs)
                
                # 检查结果
                error = self.error_detector.detect(result, None)
                if error is None:
                    # 成功，进行反思
                    reflection = self.reflexion.reflect(
                        task, "execute", str(result)
                    )
                    print(f"反思: {reflection}")
                    return result
                
                # 有错误，尝试纠正
                print(f"检测到错误: {error.message}")
                
                # 是否可以重试
                if self.retry_manager.max_retries > 0:
                    try:
                        result = await self.retry_manager.execute_with_retry(
                            executor, task, *args, **kwargs
                        )
                        return result
                    except Exception:
                        pass
                
                # 生成纠正方案
                correction = self.self_corrector.correct(
                    error, {"task": task, "attempt": attempt}
                )
                print(f"纠正方案: {correction}")
                
                # 回滚到检查点
                checkpoint = self.checkpoint_manager.get_latest_checkpoint()
                if checkpoint:
                    # 使用纠正后的参数重试
                    pass
                
                attempt += 1
            
            except Exception as e:
                print(f"执行异常: {e}")
                attempt += 1
        
        raise RuntimeError("达到最大尝试次数，任务失败")
`

## 6. 本日总结

- ErrorDetector检测执行错误
- SelfCorrector生成纠正方案
- ReflexionAgent进行反思学习
- RetryManager处理重试逻辑
- CheckpointManager支持状态回滚

明天我们将学习Context Engineering。
