'''
Day 85 示例：工作流引擎
'''

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from datetime import datetime
import asyncio


class NodeType(Enum):
    '''节点类型'''
    TASK = "task"
    CONDITION = "condition"
    PARALLEL = "parallel"
    END = "end"


@dataclass
class WorkflowNode:
    '''工作流节点'''
    id: str
    name: str
    node_type: NodeType
    handler: Callable | None = None
    next_nodes: list[str] = field(default_factory=list)


@dataclass
class Workflow:
    '''工作流'''
    name: str
    nodes: dict[str, WorkflowNode] = field(default_factory=dict)
    start_node: str = ""
    
    def add_node(self, node: WorkflowNode):
        '''添加节点'''
        self.nodes[node.id] = node
    
    def set_start(self, node_id: str):
        '''设置起始节点'''
        self.start_node = node_id


class WorkflowEngine:
    '''工作流引擎'''
    
    async def execute(self, workflow: Workflow, variables: dict = None) -> dict:
        '''执行工作流'''
        if not workflow.start_node:
            raise ValueError("未设置起始节点")
        
        vars = variables or {}
        current = workflow.start_node
        
        while current:
            node = workflow.nodes[current]
            print(f"执行: {node.name}")
            
            # 执行节点
            if node.handler:
                result = await node.handler(vars)
                vars[f"{node.id}_result"] = result
            
            # 获取下一个节点
            if node.next_nodes:
                current = node.next_nodes[0]
            else:
                current = None
        
        return vars


# 示例处理函数
async def fetch_data(vars: dict) -> str:
    '''获取数据'''
    await asyncio.sleep(0.5)
    return "获取的数据"

async def process_data(vars: dict) -> str:
    '''处理数据'''
    await asyncio.sleep(0.5)
    return "处理后的数据"

async def save_result(vars: dict) -> str:
    '''保存结果'''
    await asyncio.sleep(0.5)
    return "保存成功"


async def main():
    '''演示工作流引擎'''
    print("=" * 60)
    print("工作流引擎演示")
    print("=" * 60)
    
    # 创建工作流
    workflow = Workflow(name="数据处理流程")
    
    workflow.add_node(WorkflowNode("fetch", "获取数据", NodeType.TASK, fetch_data, ["process"]))
    workflow.add_node(WorkflowNode("process", "处理数据", NodeType.TASK, process_data, ["save"]))
    workflow.add_node(WorkflowNode("save", "保存结果", NodeType.TASK, save_result, []))
    
    workflow.set_start("fetch")
    
    # 执行
    print("\n执行工作流:")
    engine = WorkflowEngine()
    result = await engine.execute(workflow)
    
    print(f"\n执行结果: {result}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
