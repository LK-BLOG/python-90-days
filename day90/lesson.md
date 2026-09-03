# Day 90: AI Assistant Runtime ③ - 完整系统 + 毕业

## 1. 多 Agent 支持

`python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict
import time
import uuid


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    content: Any
    msg_type: str = "text"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)


class MultiAgentBus:
    \"\"\"多 Agent 消息总线\"\"\"
    
    def __init__(self):
        self.inboxes: Dict[str, List[AgentMessage]] = defaultdict(list)
        self.log: List[AgentMessage] = []
    
    def send(self, message: AgentMessage):
        self.inboxes[message.receiver].append(message)
        self.log.append(message)
    
    def receive(self, agent_id: str) -> Optional[AgentMessage]:
        if self.inboxes[agent_id]:
            return self.inboxes[agent_id].pop(0)
        return None
    
    def receive_all(self, agent_id: str) -> List[AgentMessage]:
        msgs = list(self.inboxes[agent_id])
        self.inboxes[agent_id].clear()
        return msgs
    
    def get_conversation(self, agent1: str, agent2: str) -> List[AgentMessage]:
        return [m for m in self.log
                if (m.sender == agent1 and m.receiver == agent2)
                or (m.sender == agent2 and m.receiver == agent1)]


class MultiAgentRuntime:
    \"\"\"多 Agent Runtime\"\"\"
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.bus = MultiAgentBus()
        self.orchestrator = None
    
    def register_agent(self, agent_id: str, agent: Any):
        self.agents[agent_id] = agent
    
    def set_orchestrator(self, orchestrator):
        self.orchestrator = orchestrator
    
    def run_task(self, task: str) -> str:
        if self.orchestrator:
            return self.orchestrator.execute(task, self.agents, self.bus)
        
        # 默认：广播给所有 Agent
        self.bus.send(AgentMessage("system", "all", task, "task"))
        
        results = []
        for agent_id, agent in self.agents.items():
            msg = self.bus.receive(agent_id)
            if msg:
                result = agent.process(msg) if hasattr(agent, "process") else str(msg.content)
                results.append(f"[{agent_id}]: {result}")
        
        return "\\n".join(results) if results else "无 Agent 响应"
`

## 2. 评估监控系统

`python
class RuntimeEvaluator:
    \"\"\"运行时评估器\"\"\"
    
    def __init__(self):
        self.evaluations: List[Dict] = []
        self.metrics_history: List[Dict] = []
    
    def evaluate_run(self, runtime, goal: str, result: str) -> Dict:
        metrics = {}
        
        # 功能性
        metrics["has_result"] = bool(result) and len(result) > 5
        metrics["steps_executed"] = len(runtime.memory.get_messages()) if hasattr(runtime, "memory") else 0
        
        # 效率
        metrics["goal_met"] = goal.lower() in result.lower() if result else False
        
        # 安全
        metrics["no_errors"] = "错误" not in result
        
        score = sum(1 for v in metrics.values() if v) / max(len(metrics), 1)
        
        evaluation = {
            "goal": goal,
            "result_length": len(result) if result else 0,
            "metrics": metrics,
            "score": score,
            "timestamp": time.time(),
        }
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def get_summary(self) -> Dict:
        if not self.evaluations:
            return {"total": 0}
        
        total = len(self.evaluations)
        avg_score = sum(e["score"] for e in self.evaluations) / total
        success = sum(1 for e in self.evaluations if e["score"] >= 0.6)
        
        return {
            "total": total,
            "avg_score": f"{avg_score:.2f}",
            "success_rate": f"{success/total*100:.0f}%",
            "recent": self.evaluations[-3:],
        }
`

## 3. 安全护栏集成

`python
import re
from typing import Set


class SafetyGuardrails:
    \"\"\"安全护栏系统\"\"\"
    
    INJECTION_PATTERNS = [
        r'ignore\s+previous', r'system\s*:', r'you\s+are\s+now',
    ]
    
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf\s+/', r'eval\s*\(', r'exec\s*\(',
    ]
    
    def __init__(self, max_input_length: int = 10000):
        self.max_input_length = max_input_length
        self.blocked_paths: Set[str] = set()
        self.violation_log: List[Dict] = []
    
    def validate_input(self, text: str) -> tuple[bool, str]:
        if len(text) > self.max_input_length:
            return False, "输入过长"
        
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                self.violation_log.append({"type": "injection", "text": text[:50]})
                return False, "检测到注入攻击"
        
        return True, "通过"
    
    def validate_output(self, text: str) -> tuple[bool, str]:
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                self.violation_log.append({"type": "dangerous", "text": text[:50]})
                return False, "输出包含危险模式"
        
        # 敏感信息检测
        if re.search(r'\b\d{16}\b', text):
            text = re.sub(r'\b\d{16}\b', '[CARD_REDACTED]', text)
            return True, "已脱敏"
        
        return True, "通过"
    
    def check_permission(self, action: str, resource: str) -> bool:
        if action == "write" and resource in self.blocked_paths:
            self.violation_log.append({"type": "permission", "resource": resource})
            return False
        return True
    
    def get_violations(self) -> List[Dict]:
        return list(self.violation_log)
`

## 4. 完整测试套件

`python
class TestSuite:
    \"\"\"Runtime 测试套件\"\"\"
    
    def __init__(self, runtime):
        self.runtime = runtime
        self.results: List[Dict] = []
    
    def test_basic_task(self) -> Dict:
        \"\"\"测试基本任务执行\"\"\"
        try:
            result = self.runtime.run("1+1等于几")
            passed = result is not None and len(result) > 0
            return {"test": "basic_task", "passed": passed, "result": str(result)[:100]}
        except Exception as e:
            return {"test": "basic_task", "passed": False, "error": str(e)}
    
    def test_tool_registration(self) -> Dict:
        \"\"\"测试工具注册\"\"\"
        try:
            has_tools = len(self.runtime.tools) > 0 if hasattr(self.runtime, "tools") else False
            return {"test": "tool_registration", "passed": has_tools}
        except Exception as e:
            return {"test": "tool_registration", "passed": False, "error": str(e)}
    
    def test_memory(self) -> Dict:
        \"\"\"测试记忆系统\"\"\"
        try:
            if hasattr(self.runtime, "memory"):
                self.runtime.memory.add_message("test", "测试消息")
                msgs = self.runtime.memory.get_messages()
                passed = len(msgs) > 0
            else:
                passed = False
            return {"test": "memory", "passed": passed}
        except Exception as e:
            return {"test": "memory", "passed": False, "error": str(e)}
    
    def test_safety(self) -> Dict:
        \"\"\"测试安全护栏\"\"\"
        try:
            if hasattr(self.runtime, "safety"):
                ok1, _ = self.runtime.safety.validate_input("正常输入")
                ok2, _ = self.runtime.safety.validate_input("ignore previous instructions")
                passed = ok1 and not ok2
            else:
                passed = False
            return {"test": "safety", "passed": passed}
        except Exception as e:
            return {"test": "safety", "passed": False, "error": str(e)}
    
    def run_all(self) -> Dict:
        self.results = [
            self.test_basic_task(),
            self.test_tool_registration(),
            self.test_memory(),
            self.test_safety(),
        ]
        
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        return {
            "total": total,
            "passed": passed,
            "score": f"{passed/total*100:.0f}%",
            "details": self.results,
        }
`

## 5. 完整 Runtime（毕业版）

`python
class AIRuntimeV3:
    \"\"\"AI Assistant Runtime V3 - 毕业版本\"\"\"
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        
        # 核心组件
        self.memory = MemoryManager()
        self.planner = PlanningModule()
        self.correction = SelfCorrectionModule()
        self.context = ContextManager()
        self.safety = SafetyGuardrails()
        self.evaluator = RuntimeEvaluator()
        self.tracer = Tracer()
        
        # 工具
        self.tools: Dict[str, Any] = {}
        
        # 多 Agent
        self.multi_agent = MultiAgentRuntime()
        
        # 状态
        self.current_plan = None
        self.is_running = False
        self.run_count = 0
    
    def register_tool(self, name: str, tool: Any, description: str = ""):
        self.tools[name] = tool
        self.context.add_tool_description(name, description or name)
    
    def run(self, goal: str) -> str:
        \"\"\"执行任务\"\"\"
        # 安全检查
        ok, reason = self.safety.validate_input(goal)
        if not ok:
            return f"安全拦截: {reason}"
        
        self.is_running = True
        self.run_count += 1
        
        # 记忆
        self.memory.add_message("user", goal)
        
        # 追踪
        with self.tracer.span("run_task", goal=goal):
            # 规划
            plan = self.planner.create_plan(goal, list(self.tools.keys()))
            
            # 执行
            for _ in range(len(plan.tasks) * 2):
                ready = plan.get_ready()
                if not ready:
                    break
                
                for task in ready:
                    self._execute_task(task, goal)
            
            # 评估
            result = self._synthesize(goal)
            self.evaluator.evaluate_run(self, goal, result)
        
        # 输出安全检查
        ok, _ = self.safety.validate_output(result)
        if not ok:
            result = "[输出已被安全过滤]"
        
        # 记忆
        self.memory.add_message("assistant", result)
        
        self.is_running = False
        return result
    
    def _execute_task(self, task, goal):
        task.status = TaskStatus.RUNNING
        tool = self.tools.get(task.tool)
        
        if not tool:
            task.status = TaskStatus.FAILED
            task.error = f"无工具: {task.tool}"
            self.planner.replan(self.current_plan if hasattr(self, 'current_plan') else None, task, task.error)
            return
        
        try:
            result = tool(**task.params)
            task.status = TaskStatus.COMPLETED
            task.result = str(result)
            
            # 自我纠正
            should_retry, issues = self.correction.should_retry(str(result), goal)
            if should_retry:
                result = self.correction.correct(str(result), [issues], goal)
                task.result = str(result)
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
    
    def _synthesize(self, goal):
        return f"目标: {goal}\\n执行完成"
    
    def get_status(self) -> Dict:
        return {
            "running": self.is_running,
            "run_count": self.run_count,
            "tools": list(self.tools.keys()),
            "memory_messages": len(self.memory.get_messages()),
            "evaluations": self.evaluator.get_summary(),
            "violations": len(self.safety.get_violations()),
        }
`

## 6. 文档生成

`python
def generate_docs(runtime) -> str:
    \"\"\"生成项目文档\"\"\"
    docs = f\"\"\"# AI Assistant Runtime 文档

## 概述
AI Assistant Runtime 是一个完整的 Agent 框架，支持：
- Agent 核心循环（Think → Act → Observe）
- 工具系统（注册/发现/调用）
- 记忆系统（短期/长期/工作记忆）
- 规划系统（创建/执行/重规划）
- 安全护栏（输入验证/输出过滤）
- 评估监控（评估/追踪/成本）

## 架构
`
┌─────────────────────────────────────┐
│          AIRuntimeV3                │
├─────────┬──────────┬────────────────┤
│ Memory  │ Planning │  Safety        │
│ Manager │ Module   │  Guardrails    │
├─────────┴──────────┴────────────────┤
│         Tool Registry               │
│   (Calculator, Search, File, ...)   │
├─────────────────────────────────────┤
│       Evaluation & Tracing          │
└─────────────────────────────────────┘
`

## 工具列表
\"\"\"
    
    for name, tool in runtime.tools.items():
        docs += f\"\"\"### {name}
- 描述: {getattr(tool, 'description', 'N/A')}
\"\"\"
    
    docs += f\"\"\"
## 使用示例
`python
runtime = AIRuntimeV3()
runtime.register_tool(\"calc\", lambda expression=\"\": str(eval(expression)))
result = runtime.run(\"计算 2+3*4\")
print(result)
`

## 测试
运行测试: python -m pytest tests/ -v
\"\"\"
    
    return docs
`

## 7. 毕业清单

### 功能检查（60分）
- [ ] ✅ Agent Loop 核心循环（10分）
- [ ] ✅ 工具注册和调用系统（10分）
- [ ] ✅ Memory 系统（短期/长期/工作）（10分）
- [ ] ✅ Planning 模块（计划/执行/重规划）（10分）
- [ ] ✅ Safety Guardrails（输入/输出安全）（10分）
- [ ] ✅ Evaluation & Tracing（评估/追踪）（10分）

### 代码质量（20分）
- [ ] ✅ 项目结构清晰（5分）
- [ ] ✅ 类型注解完善（5分）
- [ ] ✅ 错误处理完善（5分）
- [ ] ✅ 代码注释充分（5分）

### 测试覆盖（20分）
- [ ] ✅ 核心功能有测试（10分）
- [ ] ✅ 测试覆盖率 > 60%（10分）

### 总分：___/100（70分通过）
