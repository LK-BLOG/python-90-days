# Day 89: AI Assistant Runtime ② - 集成核心组件

## 1. Memory 集成

`python
from collections import deque
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib


class MemoryManager:
    \"\"\"统一记忆管理器\"\"\"
    
    def __init__(self, short_term_size: int = 50):
        self.short_term = deque(maxlen=short_term_size)
        self.long_term: Dict[str, str] = {}
        self.working: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str):
        self.short_term.append({"role": role, "content": content})
    
    def get_messages(self, last_n: int = None) -> List[Dict]:
        msgs = list(self.short_term)
        return msgs[-last_n:] if last_n else msgs
    
    def search(self, query: str) -> List[Dict]:
        return [m for m in self.short_term if query.lower() in m.get("content", "").lower()]
    
    def store_important(self, content: str, key: str = None):
        key = key or hashlib.md5(content.encode()).hexdigest()[:8]
        self.long_term[key] = content
    
    def get_context(self) -> str:
        recent = self.get_messages(5)
        return "\n".join([f'  [{m["role"]}]: {m["content"][:60]}' for m in recent])
    
    def clear(self, scope: str = "all"):
        if scope in ("all", "short"):
            self.short_term.clear()
        if scope in ("all", "working"):
            self.working.clear()
`

## 2. Planning 集成

`python
from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    description: str
    tool: str = ""
    params: Dict = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None


class PlanningModule:
    def create_plan(self, goal: str, available_tools: List[str]) -> 'Plan':
        if "报告" in goal or "分析" in goal:
            tasks = [
                Task("t1", "搜索数据", "web_search", {"query": goal}),
                Task("t2", "分析", "calculator", {"expression": "1+1"}, ["t1"]),
                Task("t3", "写报告", "file_write", {"content": "报告"}, ["t2"]),
            ]
        else:
            tasks = [Task("t1", f"处理: {goal}", "calculator", {"expression": "1"})]
        return Plan(goal=goal, tasks=tasks)
    
    def replan(self, plan, failed_task, error):
        alt = {"web_search": "calculator", "code_exec": "shell"}
        if failed_task.tool in alt:
            failed_task.tool = alt[failed_task.tool]
            failed_task.status = TaskStatus.PENDING
        return plan


class Plan:
    def __init__(self, goal, tasks):
        self.goal = goal
        self.tasks = tasks
    
    def get_ready(self):
        done = {t.id for t in self.tasks if t.status == TaskStatus.COMPLETED}
        return [t for t in self.tasks if t.status == TaskStatus.PENDING
                and all(d in done for d in t.depends_on)]
    
    def is_complete(self):
        return all(t.status == TaskStatus.COMPLETED for t in self.tasks)
`

## 3. Self-Correction 模块

`python
class SelfCorrectionModule:
    def __init__(self, max_corrections: int = 3):
        self.max_corrections = max_corrections
        self.history: List[Dict] = []
    
    def check_output(self, output: str, goal: str) -> List[str]:
        issues = []
        if len(output) < 10:
            issues.append("输出太短")
        if "TODO" in output:
            issues.append("包含未完成标记")
        return issues
    
    def correct(self, output: str, issues: list, goal: str) -> str:
        self.history.append({"original": output, "issues": issues})
        if "输出太短" in issues:
            output = f"{output} [已补充]"
        return output
    
    def should_retry(self, output: str, goal: str) -> tuple:
        issues = self.check_output(output, goal)
        if not issues:
            return False, ""
        if len(self.history) >= self.max_corrections:
            return False, "已达最大纠正次数"
        return True, "; ".join(issues)
`

## 4. Context Engineering 集成

`python
class ContextManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.system_prompt = ""
        self.tool_descriptions: List[str] = []
    
    def add_tool_description(self, name, description, params=""):
        self.tool_descriptions.append(f"- {name}: {description} ({params})")
    
    def build_context(self, memory: MemoryManager, goal: str) -> str:
        parts = []
        if self.system_prompt:
            parts.append(self.system_prompt)
        if self.tool_descriptions:
            parts.append("工具:\n" + "\n".join(self.tool_descriptions))
        ctx = memory.get_context()
        if ctx:
            parts.append(f"历史:\n{ctx}")
        parts.append(f"目标: {goal}")
        return "\n\n---\n\n".join(parts)
`

## 5. 状态管理

`python
import time
import copy

class StateManager:
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.history: List[Dict] = []
        self.version = 0
    
    def save(self, name=""):
        self.history.append({"version": self.version, "name": name, "state": copy.deepcopy(self.state), "time": time.time()})
        self.version += 1
    
    def update(self, key, value):
        self.state[key] = value
    
    def get(self, key, default=None):
        return self.state.get(key, default)
    
    def rollback(self, version=None):
        if not self.history:
            return False
        if version is None:
            snap = self.history.pop()
        else:
            for i, h in enumerate(self.history):
                if h["version"] == version:
                    snap = self.history.pop(i); break
            else:
                return False
        self.state = copy.deepcopy(snap["state"])
        return True
`

## 6. 统一 Runtime 集成

`python
class AssistantRuntime:
    \"\"\"AI Assistant Runtime V2\"\"\"
    
    def __init__(self, config=None):
        self.memory = MemoryManager()
        self.planner = PlanningModule()
        self.correction = SelfCorrectionModule()
        self.context = ContextManager()
        self.state = StateManager()
        self.tools: Dict[str, Any] = {}
        self.current_plan = None
        self.is_running = False
    
    def register_tool(self, name, tool, description=""):
        self.tools[name] = tool
        self.context.add_tool_description(name, description or name)
    
    def run(self, goal: str) -> str:
        self.is_running = True
        self.memory.add_message("user", goal)
        self.state.save("init")
        self.state.update("goal", goal)
        
        # 规划
        plan = self.planner.create_plan(goal, list(self.tools.keys()))
        
        # 执行
        for _ in range(len(plan.tasks) * 2):
            ready = plan.get_ready()
            if not ready:
                if plan.is_complete(): break
                return "计划无法继续"
            
            for task in ready:
                self._execute_task(task, goal, plan)
        
        result = self._synthesize(goal, plan)
        self.memory.add_message("assistant", result)
        self.is_running = False
        return result
    
    def _execute_task(self, task, goal, plan):
        task.status = TaskStatus.RUNNING
        tool = self.tools.get(task.tool)
        if not tool:
            task.status = TaskStatus.FAILED
            self.planner.replan(plan, task, f"无工具: {task.tool}")
            return
        
        try:
            result = tool(**task.params)
            task.status = TaskStatus.COMPLETED
            task.result = str(result)
            
            # 纠正
            should_retry, issues = self.correction.should_retry(str(result), goal)
            if should_retry:
                result = self.correction.correct(str(result), [issues], goal)
                task.result = str(result)
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = str(e)
    
    def _synthesize(self, goal, plan):
        output = f"目标: {goal}\n结果:\n"
        for t in plan.tasks:
            icon = "✅" if t.status == TaskStatus.COMPLETED else "❌"
            output += f"  {icon} {t.description}: {t.result}\n"
        return output
`

## 7. 今日目标

### 实现清单
1. ✅ Memory 集成
2. ✅ Planning 集成
3. ✅ Self-Correction
4. ✅ Context Engineering
5. ✅ State Management
6. ✅ 统一 Runtime

### 测试
`python
runtime = AssistantRuntime()
runtime.register_tool("calc", lambda expression="": str(eval(expression)), "计算")
result = runtime.run("计算 2+3*4")
assert result is not None
`

## 8. 常见错误

1. **组件不集成**：每个模块独立工作但不协作 → 统一 Runtime 串联
2. **状态不一致**：Memory 和 State 不同步 → 统一状态更新
3. **纠正死循环**：纠正后还是失败 → 设置最大纠正次数
4. **上下文溢出**：Context Manager 没控制好 token → 定期检查预算

## 9. 动手练习

### 练习 1：将 Memory 集成到 Runtime
### 练习 2：实现 Planning 执行循环
### 练习 3：添加 Self-Correction
