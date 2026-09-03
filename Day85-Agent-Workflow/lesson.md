# Day 85 课程：Agent 工作流

## 1. 工作流定义

`python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Awaitable
from datetime import datetime
import asyncio


class NodeType(Enum):
    '''节点类型'''
    START = "start"
    END = "end"
    TASK = "task"
    CONDITION = "condition"
    PARALLEL = "parallel"
    HUMAN = "human"


@dataclass
class WorkflowNode:
    '''工作流节点'''
    id: str
    name: str
    node_type: NodeType
    handler: Callable | None = None
    config: dict = field(default_factory=dict)
    next_nodes: list[str] = field(default_factory=list)
    conditions: dict[str, str] = field(default_factory=dict)  # condition -> next_node


@dataclass
class WorkflowEdge:
    '''工作流边'''
    from_node: str
    to_node: str
    condition: str | None = None


@dataclass
class WorkflowDefinition:
    '''工作流定义'''
    name: str
    description: str
    nodes: dict[str, WorkflowNode] = field(default_factory=dict)
    edges: list[WorkflowEdge] = field(default_factory=list)
    start_node: str = ""
    
    def add_node(self, node: WorkflowNode):
        '''添加节点'''
        self.nodes[node.id] = node
    
    def add_edge(self, from_node: str, to_node: str, condition: str = None):
        '''添加边'''
        self.edges.append(WorkflowEdge(from_node, to_node, condition))
        
        # 更新节点的next_nodes
        if condition is None:
            self.nodes[from_node].next_nodes.append(to_node)
        else:
            self.nodes[from_node].conditions[condition] = to_node
    
    def get_next_nodes(self, node_id: str, context: dict = None) -> list[str]:
        '''获取下一个节点'''
        node = self.nodes[node_id]
        
        if node.node_type == NodeType.CONDITION and context:
            # 条件分支
            for condition, next_node in node.conditions.items():
                if self._evaluate_condition(condition, context):
                    return [next_node]
            return []
        
        return node.next_nodes
    
    def _evaluate_condition(self, condition: str, context: dict) -> bool:
        '''评估条件'''
        # 简单的条件评估
        # 实际实现中，这里可以使用更复杂的逻辑
        return context.get(condition, False)
`

## 2. 工作流执行引擎

`python
@dataclass
class WorkflowState:
    '''工作流状态'''
    workflow_name: str
    current_node: str
    node_states: dict[str, str] = field(default_factory=dict)  # node_id -> state
    variables: dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None


class WorkflowEngine:
    '''工作流引擎'''
    
    def __init__(self):
        self.workflows: dict[str, WorkflowDefinition] = {}
        self.states: dict[str, WorkflowState] = {}
    
    def register_workflow(self, workflow: WorkflowDefinition):
        '''注册工作流'''
        self.workflows[workflow.name] = workflow
    
    async def execute(self, workflow_name: str, initial_vars: dict = None) -> WorkflowState:
        '''执行工作流'''
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"工作流不存在: {workflow_name}")
        
        # 创建状态
        state = WorkflowState(
            workflow_name=workflow_name,
            current_node=workflow.start_node,
            variables=initial_vars or {}
        )
        
        self.states[workflow_name] = state
        
        # 执行工作流
        while state.current_node:
            node = workflow.nodes[state.current_node]
            
            print(f"执行节点: {node.name} ({node.node_type.value})")
            
            # 根据节点类型执行
            if node.node_type == NodeType.END:
                state.completed_at = datetime.now()
                break
            
            elif node.node_type == NodeType.TASK:
                if node.handler:
                    result = await node.handler(state.variables)
                    state.variables[f"{node.id}_result"] = result
                state.node_states[node.id] = "completed"
            
            elif node.node_type == NodeType.PARALLEL:
                await self._execute_parallel(node, state)
            
            elif node.node_type == NodeType.HUMAN:
                await self._wait_for_human(node, state)
            
            # 获取下一个节点
            next_nodes = workflow.get_next_nodes(state.current_node, state.variables)
            
            if next_nodes:
                state.current_node = next_nodes[0]
            else:
                state.current_node = None
        
        return state
    
    async def _execute_parallel(self, node: WorkflowNode, state: WorkflowState):
        '''执行并行节点'''
        tasks = []
        for next_node_id in node.next_nodes:
            # 创建并行任务
            task = asyncio.create_task(
                self._execute_node(next_node_id, state)
            )
            tasks.append(task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"并行任务 {node.next_nodes[i]} 失败: {result}")
            else:
                state.variables[f"{node.next_nodes[i]}_result"] = result
    
    async def _execute_node(self, node_id: str, state: WorkflowState):
        '''执行单个节点'''
        workflow = self.workflows[state.workflow_name]
        node = workflow.nodes[node_id]
        
        if node.handler:
            return await node.handler(state.variables)
        return None
    
    async def _wait_for_human(self, node: WorkflowNode, state: WorkflowState):
        '''等待人工介入'''
        print(f"等待人工介入: {node.name}")
        print(f"当前状态: {state.variables}")
        
        # 实际实现中，这里应该等待人工输入
        # 这里简化为等待一小段时间
        await asyncio.sleep(1)
        
        # 模拟人工输入
        state.variables[f"{node.id}_human_input"] = "人工输入的内容"
`

## 3. 条件分支

`python
class ConditionalNode:
    '''条件节点'''
    
    def __init__(self, node_id: str, name: str):
        self.node_id = node_id
        self.name = name
        self.branches: list[tuple[Callable, str]] = []  # (condition_func, next_node)
        self.default_branch: str | None = None
    
    def add_branch(self, condition: Callable, next_node: str):
        '''添加分支'''
        self.branches.append((condition, next_node))
    
    def set_default(self, next_node: str):
        '''设置默认分支'''
        self.default_branch = next_node
    
    def evaluate(self, context: dict) -> str | None:
        '''评估条件'''
        for condition_func, next_node in self.branches:
            if condition_func(context):
                return next_node
        return self.default_branch


# 条件函数示例
def is_high_priority(context: dict) -> bool:
    '''是否高优先级'''
    return context.get("priority", 0) > 7

def has_data(context: dict) -> bool:
    '''是否有数据'''
    return bool(context.get("data"))

def is_error(context: dict) -> bool:
    '''是否出错'''
    return context.get("error") is not None
`

## 4. Human-in-the-Loop

`python
from enum import Enum
import uuid


class HumanAction(Enum):
    '''人工操作类型'''
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    SKIP = "skip"


@dataclass
class HumanRequest:
    '''人工请求'''
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str = ""
    description: str = ""
    data: Any = None
    created_at: datetime = field(default_factory=datetime.now)
    completed: bool = False
    action: HumanAction | None = None
    response: Any = None


class HumanInTheLoopManager:
    '''人工介入管理器'''
    
    def __init__(self):
        self.pending_requests: list[HumanRequest] = []
        self.completed_requests: list[HumanRequest] = []
    
    def request_approval(
        self, 
        node_id: str, 
        description: str, 
        data: Any
    ) -> HumanRequest:
        '''请求批准'''
        request = HumanRequest(
            node_id=node_id,
            description=description,
            data=data
        )
        self.pending_requests.append(request)
        return request
    
    def get_pending(self) -> list[HumanRequest]:
        '''获取待处理请求'''
        return [r for r in self.pending_requests if not r.completed]
    
    def respond(
        self, 
        request_id: str, 
        action: HumanAction, 
        response: Any = None
    ):
        '''响应请求'''
        for request in self.pending_requests:
            if request.id == request_id:
                request.completed = True
                request.action = action
                request.response = response
                self.completed_requests.append(request)
                break
    
    async def wait_for_response(self, request: HumanRequest, timeout: int = 300):
        '''等待响应'''
        start_time = datetime.now()
        
        while not request.completed:
            if (datetime.now() - start_time).total_seconds() > timeout:
                raise TimeoutError("等待人工响应超时")
            await asyncio.sleep(1)
        
        return request.action, request.response
`

## 5. 工作流编排引擎

`python
class WorkflowOrchestrator:
    '''工作流编排器'''
    
    def __init__(self, engine: WorkflowEngine = None):
        self.engine = engine or WorkflowEngine()
        self.human_manager = HumanInTheLoopManager()
        self.workflow_history: list[dict] = []
    
    def create_workflow_from_dag(self, dag: dict) -> WorkflowDefinition:
        '''从DAG创建工作流'''
        workflow = WorkflowDefinition(
            name=dag.get("name", "unnamed"),
            description=dag.get("description", "")
        )
        
        # 添加节点
        for node_data in dag.get("nodes", []):
            node = WorkflowNode(
                id=node_data["id"],
                name=node_data.get("name", node_data["id"]),
                node_type=NodeType(node_data.get("type", "task")),
                handler=node_data.get("handler")
            )
            workflow.add_node(node)
        
        # 添加边
        for edge_data in dag.get("edges", []):
            workflow.add_edge(
                edge_data["from"],
                edge_data["to"],
                edge_data.get("condition")
            )
        
        # 设置起始节点
        workflow.start_node = dag.get("start", "")
        
        return workflow
    
    async def execute_workflow(
        self, 
        workflow_name: str, 
        variables: dict = None
    ) -> dict:
        '''执行工作流'''
        result = await self.engine.execute(workflow_name, variables)
        
        self.workflow_history.append({
            "workflow": workflow_name,
            "started_at": result.started_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "variables": result.variables
        })
        
        return result.variables
`

## 6. 本日总结

- WorkflowDefinition定义工作流结构
- WorkflowEngine执行工作流
- ConditionalNode实现条件分支
- HumanInTheLoopManager管理人工介入
- WorkflowOrchestrator编排复杂工作流

明天我们将学习评估与追踪。
