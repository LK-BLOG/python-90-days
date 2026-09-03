# Day 85: Agent 工作流

## 1. 工作流定义

### 1.1 DAG（有向无环图）

`python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional
from enum import Enum
from collections import defaultdict


class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_HUMAN = "waiting_human"


@dataclass
class WorkflowNode:
    \"\"\"工作流节点\"\"\"
    id: str
    name: str
    node_type: str = "action"  # action, condition, human_input, parallel
    handler: Callable = None
    params: Dict = field(default_factory=dict)
    status: NodeStatus = NodeStatus.PENDING
    result: Any = None
    edges: List[str] = field(default_factory=list)  # 出边（下一节点ID）
    condition: str = ""  # 条件节点的判断逻辑


class DAG:
    \"\"\"有向无环图\"\"\"
    
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = defaultdict(list)
        self.reverse_edges: Dict[str, List[str]] = defaultdict(list)
    
    def add_node(self, node: WorkflowNode):
        self.nodes[node.id] = node
    
    def add_edge(self, from_id: str, to_id: str, condition: str = ""):
        self.edges[from_id].append(to_id)
        self.reverse_edges[to_id].append(from_id)
        if condition:
            self.nodes[from_id].condition = condition
    
    def get_root_nodes(self) -> List[str]:
        \"\"\"获取没有入边的节点（起点）\"\"\"
        return [
            nid for nid in self.nodes
            if not self.reverse_edges[nid]
        ]
    
    def get_downstream(self, node_id: str) -> List[str]:
        return self.edges.get(node_id, [])
    
    def topological_sort(self) -> List[str]:
        \"\"\"拓扑排序\"\"\"
        in_degree = {nid: len(self.reverse_edges[nid]) for nid in self.nodes}
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in self.edges.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.nodes):
            raise ValueError("图中存在循环！")
        
        return result
    
    def validate(self) -> tuple:
        \"\"\"验证 DAG\"\"\"
        try:
            self.topological_sort()
            return True, "DAG 有效"
        except ValueError as e:
            return False, str(e)
`

## 2. 状态机工作流

`python
class StateMachine:
    \"\"\"状态机\"\"\"
    
    def __init__(self):
        self.states: Dict[str, dict] = {}
        self.transitions: List[dict] = []
        self.current_state: str = ""
        self.history: List[str] = []
    
    def add_state(self, name: str, on_enter: Callable = None, on_exit: Callable = None):
        self.states[name] = {
            "on_enter": on_enter,
            "on_exit": on_exit,
        }
    
    def add_transition(self, from_state: str, to_state: str, condition: str = ""):
        self.transitions.append({
            "from": from_state,
            "to": to_state,
            "condition": condition,
        })
    
    def start(self, initial_state: str):
        self.current_state = initial_state
        self.history = [initial_state]
        state = self.states.get(initial_state)
        if state and state["on_enter"]:
            state["on_enter"]()
    
    def transition(self, to_state: str) -> bool:
        # 检查是否有有效的转移
        valid = any(
            t["from"] == self.current_state and t["to"] == to_state
            for t in self.transitions
        )
        
        if not valid:
            return False
        
        # 执行 on_exit
        current = self.states.get(self.current_state)
        if current and current["on_exit"]:
            current["on_exit"]()
        
        self.current_state = to_state
        self.history.append(to_state)
        
        # 执行 on_enter
        target = self.states.get(to_state)
        if target and target["on_enter"]:
            target["on_enter"]()
        
        return True
`

## 3. Human-in-the-Loop

`python
class HumanInTheLoop:
    \"\"\"Human-in-the-Loop 工作流\"\"\"
    
    def __init__(self):
        self.pending_requests: List[dict] = []
        self.approved: Dict[str, bool] = {}
    
    def request_approval(self, request_id: str, description: str, data: Any = None):
        \"\"\"请求人类批准\"\"\"
        self.pending_requests.append({
            "id": request_id,
            "description": description,
            "data": data,
            "status": "pending",
        })
        print(f"⏸ 等待人工审批: {description}")
    
    def approve(self, request_id: str, approved: bool = True, feedback: str = ""):
        \"\"\"人类批准/拒绝\"\"\"
        self.approved[request_id] = approved
        for req in self.pending_requests:
            if req["id"] == request_id:
                req["status"] = "approved" if approved else "rejected"
                req["feedback"] = feedback
                break
    
    def is_approved(self, request_id: str) -> bool:
        return self.approved.get(request_id, False)
    
    def get_pending(self) -> List[dict]:
        return [r for r in self.pending_requests if r["status"] == "pending"]
    
    def execute_with_approval(self, task_id: str, action: Callable, description: str) -> Any:
        \"\"\"需要批准才能执行的操作\"\"\"
        self.request_approval(task_id, description)
        
        # 模拟等待
        import time
        for _ in range(10):
            if task_id in self.approved:
                break
            time.sleep(0.1)
        
        if not self.is_approved(task_id):
            return None
        
        return action()
`

## 4. 工作流编排引擎

`python
class WorkflowEngine:
    \"\"\"工作流编排引擎\"\"\"
    
    def __init__(self):
        self.dag = DAG()
        self.state_machine = StateMachine()
        self.human_loop = HumanInTheLoop()
    
    def execute(self) -> str:
        \"\"\"执行工作流\"\"\"
        roots = self.dag.get_root_nodes()
        executed = set()
        results = {}
        
        def execute_node(node_id: str):
            if node_id in executed:
                return results.get(node_id)
            
            # 检查依赖
            deps = self.dag.reverse_edges.get(node_id, [])
            for dep in deps:
                if dep not in executed:
                    execute_node(dep)
            
            node = self.dag.nodes[node_id]
            print(f"▶ 执行节点: {node.name}")
            
            # 如果是人工节点
            if node.node_type == "human_input":
                self.human_loop.request_approval(node_id, node.name, node.params)
                # 等待审批...
            
            # 执行
            if node.handler:
                result = node.handler(**node.params)
                node.result = result
                node.status = NodeStatus.COMPLETED
                results[node_id] = result
                print(f"  ✅ 完成: {str(result)[:80]}")
            else:
                node.status = NodeStatus.COMPLETED
                results[node_id] = None
            
            executed.add(node_id)
            
            # 执行下游
            for next_id in self.dag.get_downstream(node_id):
                execute_node(next_id)
        
        for root in roots:
            execute_node(root)
        
        return f"工作流完成，执行了 {len(executed)} 个节点"
`

## 5. 常见错误

1. **循环依赖**：DAG 中有环 → 拓扑排序检测
2. **孤立节点**：有节点没被连接 → 验证连通性
3. **Human 等太久**：审批流程卡住 → 设置超时
4. **状态不一致**：并行节点冲突 → 用锁或状态机
5. **错误传播**：一个节点失败影响全局 → 添加错误处理

## 6. 动手练习

### 练习 1：实现 DAG 数据结构
### 练习 2：实现状态机
### 练习 3：实现工作流编排引擎
