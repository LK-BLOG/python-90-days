# Day 89: AI Assistant Runtime ② - 集成核心组件

## 1. Memory 集成

`python
from collections import deque
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import re


class MemoryManager:
    \"\"\"统一记忆管理器\"\"\"
    
    def __init__(self, short_term_size: int = 50, long_term_path: str = None):
        # 短期记忆
        self.short_term = deque(maxlen=short_term_size)
        
        # 长期记忆
        self.long_term_path = Path(long_term_path) if long_term_path else None
        self.long_term = {}
        
        # 工作记忆
        self.working: Dict[str, Any] = {}
        
        if self.long_term_path and self.long_term_path.exists():
            self._load_long_term()
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        self.short_term.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
        })
    
    def get_messages(self, last_n: int = None) -> List[Dict]:
        msgs = list(self.short_term)
        return msgs[-last_n:] if last_n else msgs
    
    def search(self, query: str) -> List[Dict]:
        results = []
        for msg in self.short_term:
            if query.lower() in msg.get("content", "").lower():
                results.append(msg)
        return results
    
    def store_important(self, content: str, key: str = None):
        key = key or hashlib.md5(content.encode()).hexdigest()[:8]
        self.long_term[key] = {"content": content, "importance": "high"}
        self._save_long_term()
    
    def recall(self, query: str, scope: str = "all") -> List[Dict]:
        results = []
        if scope in ("all", "short"):
            results.extend(self.search(query))
        if scope in ("all", "long"):
            for key, entry in self.long_term.items():
                if query.lower() in entry["content"].lower():
                    results.append({"source": "long_term", **entry})
        return results
    
    def get_context(self) -> str:
        parts = []
        if self.working:
            parts.append(f"[工作记忆] {json.dumps(self.working, ensure_ascii=False)}")
        recent = self.get_messages(last_n=5)
        if recent:
            history = "\\n".join([f"  [{m['role']}]: {m['content'][:80]}" for m in recent])
            parts.append(f"[短期记忆]\\n{history}")
        return "\\n\\n".join(parts) if parts else "无记忆"
    
    def set_working(self, key: str, value: Any):
        self.working[key] = value
    
    def get_working(self, key: str, default=None):
        return self.working.get(key, default)
    
    def clear(self, scope: str = "all"):
        if scope in ("all", "short"):
            self.short_term.clear()
        if scope in ("all", "working"):
            self.working.clear()
    
    def _save_long_term(self):
        if self.long_term_path:
            self.long_term_path.parent.mkdir(parents=True, exist_ok=True)
            self.long_term_path.write_text(json.dumps(self.long_term, ensure_ascii=False))
    
    def _load_long_term(self):
        if self.long_term_path.exists():
            self.long_term = json.loads(self.long_term_path.read_text())
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
    error: str = ""


@dataclass
class Plan:
    goal: str
    tasks: List[Task]
    
    def get_ready(self) -> List[Task]:
        done = {t.id for t in self.tasks if t.status == TaskStatus.COMPLETED}
        return [t for t in self.tasks if t.status == TaskStatus.PENDING
                and all(d in done for d in t.depends_on)]
    
    def is_complete(self) -> bool:
        return all(t.status == TaskStatus.COMPLETED for t in self.tasks)


class PlanningModule:
    \"\"\"规划模块\"\"\"
    
    def create_plan(self, goal: str, available_tools: List[str]) -> Plan:
        # 模拟 LLM 生成计划
        if "报告" in goal or "分析" in goal:
            tasks = [
                Task("t1", "搜索数据", "web_search", {"query": goal}),
                Task("t2", "分析数据", "calculator", {"expression": "1+1"}, ["t1"]),
                Task("t3", "生成报告", "file_write", {"content": "报告"}, ["t2"]),
            ]
        elif "代码" in goal or "程序" in goal:
            tasks = [
                Task("t1", "分析需求", "calculator", {"expression": "1"}),
                Task("t2", "编写代码", "code_exec", {"code": "print('hello')"}, ["t1"]),
                Task("t3", "测试", "shell", {"command": "echo test"}, ["t2"]),
            ]
        else:
            tasks = [
                Task("t1", f"处理: {goal}", "calculator", {"expression": "1"}),
            ]
        
        return Plan(goal=goal, tasks=tasks)
    
    def replan(self, plan: Plan, failed_task: Task, error: str) -> Plan:
        # 简单重规划：替换工具
        alt_tools = {"web_search": "calculator", "code_exec": "shell"}
        if failed_task.tool in alt_tools:
            failed_task.tool = alt_tools[failed_task.tool]
            failed_task.status = TaskStatus.PENDING
            failed_task.error = ""
        return plan
`

## 3. Self-Correction 模块

`python
class SelfCorrectionModule:
    \"\"\"自我纠正模块\"\"\"
    
    def __init__(self, max_corrections: int = 3):
        self.max_corrections = max_corrections
        self.correction_history: List[Dict] = []
    
    def check_output(self, output: str, goal: str) -> List[str]:
        \"\"\"检查输出质量\"\"\"
        issues = []
        
        if len(output) < 10:
            issues.append("输出太短")
        if "TODO" in output:
            issues.append("包含未完成标记")
        if "错误" in output and "完成" not in output:
            issues.append("包含错误信息")
        
        return issues
    
    def correct(self, output: str, issues: List[str], goal: str) -> str:
        \"\"\"纠正输出\"\"\"
        self.correction_history.append({
            "original": output,
            "issues": issues,
            "corrected_at": len(self.correction_history),
        })
        
        # 模拟纠正
        if "输出太短" in issues:
            output = f"{output} [已补充详细信息]"
        if "包含错误" in issues:
            output = output.replace("错误", "已修复")
        
        return output
    
    def should_retry(self, output: str, goal: str) -> tuple[bool, str]:
        \"\"\"是否需要重试\"\"\"
        issues = self.check_output(output, goal)
        
        if not issues:
            return False, ""
        
        if len(self.correction_history) >= self.max_corrections:
            return False, f"已达到最大纠正次数 ({self.max_corrections})"
        
        return True, "; ".join(issues)
`

## 4. Context Engineering 集成

`python
class ContextManager:
    \"\"\"上下文管理器\"\"\"
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.system_prompt = ""
        self.tool_descriptions: List[str] = []
    
    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
    
    def add_tool_description(self, name: str, description: str, params: str = ""):
        self.tool_descriptions.append(f"- {name}: {description} ({params})")
    
    def build_context(self, memory: MemoryManager, current_goal: str) -> str:
        \"\"\"构建上下文\"\"\"
        parts = []
        
        # System prompt
        if self.system_prompt:
            parts.append(self.system_prompt)
        
        # 工具描述
        if self.tool_descriptions:
            tools_text = "\\n".join(self.tool_descriptions)
            parts.append(f"可用工具:\\n{tools_text}")
        
        # 记忆上下文
        memory_context = memory.get_context()
        if memory_context:
            parts.append(f"对话历史:\\n{memory_context}")
        
        # 当前目标
        parts.append(f"当前目标: {current_goal}")
        
        # 截断到 token 预算（粗略估计）
        full_context = "\\n\\n---\\n\\n".join(parts)
        estimated_tokens = len(full_context) // 4
        
        if estimated_tokens > self.max_tokens:
            # 压缩记忆部分
            messages = memory.get_messages(last_n=5)
            compressed = messages[-3:] if len(messages) > 3 else messages
            memory_text = "\\n".join([f"[{m['role']}]: {m['content'][:60]}" for m in compressed])
            parts[-2] = f"最近对话:\\n{memory_text}"
            full_context = "\\n\\n---\\n\\n".join(parts)
        
        return full_context
`

## 5. 状态管理集成

`python
import time
import copy


class StateManager:
    \"\"\"状态管理器 - 支持检查点和回滚\"\"\"
    
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.history: List[Dict] = []
        self.version = 0
    
    def save(self, name: str = ""):
        self.history.append({
            "version": self.version,
            "name": name,
            "state": copy.deepcopy(self.state),
            "timestamp": time.time(),
        })
        self.version += 1
    
    def update(self, key: str, value: Any):
        self.state[key] = value
    
    def get(self, key: str, default=None):
        return self.state.get(key, default)
    
    def rollback(self, version: int = None) -> bool:
        if not self.history:
            return False
        
        if version is None:
            snapshot = self.history.pop()
        else:
            for i, h in enumerate(self.history):
                if h["version"] == version:
                    snapshot = self.history.pop(i)
                    break
            else:
                return False
        
        self.state = copy.deepcopy(snapshot["state"])
        return True
    
    def get_state(self) -> Dict:
        return dict(self.state)
`

## 6. 统一 Runtime 集成

`python
class AssistantRuntime:
    \"\"\"AI Assistant Runtime - Day 89 集成版本\"\"\"
    
    def __init__(self, config=None):
        # 核心组件
        self.memory = MemoryManager()
        self.planner = PlanningModule()
        self.correction = SelfCorrectionModule()
        self.context = ContextManager()
        self.state = StateManager()
        
        # 工具
        self.tools: Dict[str, Any] = {}
        
        # 状态
        self.current_plan = None
        self.is_running = False
    
    def register_tool(self, name: str, tool: Any):
        self.tools[name] = tool
        self.context.add_tool_description(name, getattr(tool, 'description', name))
    
    def run(self, goal: str) -> str:
        \"\"\"执行任务\"\"\"
        self.is_running = True
        self.memory.add_message("user", goal)
        
        print(f"🤖 开始执行: {goal}")
        
        # 1. 创建计划
        self.current_plan = self.planner.create_plan(goal, list(self.tools.keys()))
        print(f"📋 计划: {len(self.current_plan.tasks)} 个步骤")
        
        # 2. 保存初始状态
        self.state.save("初始状态")
        self.state.update("goal", goal)
        
        # 3. 逐步执行
        for i in range(len(self.current_plan.tasks) * 2):  # 允许重试
            ready = self.current_plan.get_ready()
            if not ready:
                if self.current_plan.is_complete():
                    break
                return "计划无法继续执行"
            
            for task in ready:
                self._execute_task(task, goal)
        
        # 4. 汇总结果
        result = self._synthesize(goal)
        self.memory.add_message("assistant", result)
        
        self.is_running = False
        return result
    
    def _execute_task(self, task: Task, goal: str):
        task.status = TaskStatus.RUNNING
        print(f"  ▶ {task.description}")
        
        tool = self.tools.get(task.tool)
        if not tool:
            task.status = TaskStatus.FAILED
            task.error = f"工具不存在: {task.tool}"
            self.planner.replan(self.current_plan, task, task.error)
            return
        
        # 参数处理
        params = dict(task.params)
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("$"):
                ref = value[1:]
                params[key] = self.state.get(ref, value)
        
        try:
            result = tool(**params)
            task.status = TaskStatus.COMPLETED
            task.result = str(result)
            self.state.update(task.id, result)
            
            # 自我纠正检查
            should_retry, issues = self.correction.should_retry(str(result), goal)
            if should_retry:
                print(f"    ⚠️ 需要修正: {issues}")
                result = self.correction.correct(str(result), [issues], goal)
                task.result = result
            
            print(f"    ✅ 完成: {str(result)[:60]}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"    ❌ 失败: {e}")
    
    def _synthesize(self, goal: str) -> str:
        if not self.current_plan:
            return "无计划"
        
        output = f"目标: {goal}\\n结果:\\n"
        for task in self.current_plan.tasks:
            status = "✅" if task.status == TaskStatus.COMPLETED else "❌"
            output += f"  {status} {task.description}: {task.result or task.error}\\n"
        return output
`

## 7. 今日目标

### 实现清单
1. ✅ Memory 集成（短期/长期/工作记忆）
2. ✅ Planning 集成（创建计划/执行/重规划）
3. ✅ Self-Correction（检查/纠正/重试）
4. ✅ Context Engineering（构建上下文/预算控制）
5. ✅ State Management（状态/检查点/回滚）
6. ✅ 统一 Runtime 集成

### 测试要求
`python
runtime = AssistantRuntime()
runtime.register_tool("calc", lambda expression="": str(eval(expression)))
result = runtime.run("计算 2+3*4")
assert result is not None
assert len(runtime.memory.get_messages()) > 0
assert runtime.state.get("goal") == "计算 2+3*4"
`
"@ | Out-File -Encoding utf8 "D:\Python-Learn-30-days\day89\lesson.md"

@"
# Day 89 挑战任务
## 挑战 1: Memory 集成
将记忆系统集成到 Runtime。

## 挑战 2: Planning 集成
实现计划的创建和执行。

## 挑战 3: Self-Correction
实现输出质量检查和纠正。

## 挑战 4: Context Engineering
实现动态上下文构建。

## 挑战 5（Boss）: 完整 Runtime ②
集成所有组件到统一的 Runtime。
