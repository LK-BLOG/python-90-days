# Day 29 课程：AI + Agent 开发全指南

## 第一部分：LLM API基础

### 1.1 什么是LLM API

LLM（大语言模型）API是通过HTTP请求与AI模型交互的接口。OpenAI定义了事实标准，几乎所有AI服务商都兼容这个格式。

核心概念：
- **Model**: 模型名称，如 gpt-4o, gpt-3.5-turbo
- **Message**: 消息对象，包含 role 和 content
- **Token**: 文本的基本单位，约3/4个英文单词 = 1 token，中文约1-2字 = 1 token
- **Temperature**: 控制输出随机性，0=确定性，1=创造性
- **Max Tokens**: 限制生成的最大token数

### 1.2 Chat Completion API格式

`python
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="your-key")

response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "什么是Python？"},
    ],
    temperature=0.7,
    max_tokens=1000,
)

# 响应结构
print(response.choices[0].message.content)  # 模型回复
print(response.usage.total_tokens)           # token用量
`

### 1.3 用httpx/aiohttp直接调用

`python
import httpx

async def call_openai_direct(messages: list[dict]) -> str:
    """不使用SDK，直接HTTP调用"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o",
                "messages": messages,
                "temperature": 0.7,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
`

### 1.4 流式输出（Streaming）

`python
async def stream_chat(prompt: str):
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
`

---

## 第二部分：Prompt Engineering

### 2.1 System Prompt（系统提示）

系统提示定义AI的角色、行为边界和输出格式：

`python
messages = [
    {
        "role": "system",
        "content": """你是一个Python高级教学助手。
规则：
1. 用简洁中文回答
2. 给出可运行的代码示例
3. 如果不确定就说不知道，不要编造
4. 输出格式：先解释，再代码，最后总结"""
    }
]
`

### 2.2 Few-shot Learning（少样本学习）

给几个示例，让模型学会你要的格式：

`python
messages = [
    {
        "role": "system",
        "content": """将自然语言转换为SQL查询。

示例：
用户：查询所有年龄大于30的用户
SQL: SELECT * FROM users WHERE age > 30

用户：统计每个城市的用户数量
SQL: SELECT city, COUNT(*) FROM users GROUP BY city

现在请转换："""
    },
    # 少样本示例直接写在system里或作为assistant消息
]
`

### 2.3 Chain-of-Thought（思维链）

引导模型分步思考：

`python
messages = [
    {
        "role": "user",
        "content": """请一步步分析这个代码的问题：

`python
def find_max(lst):
    max_val = 0
    for x in lst:
        if x > max_val:
            max_val = x
    return max_val
`

请：
1. 列出代码做了什么
2. 找出可能的bug
3. 给出修复方案"""
    }
]
`

### 2.4 结构化输出

`python
messages = [
    {
        "role": "system",
        "content": """分析代码并以JSON格式返回：
{
    "issues": [{"type": "bug|warning|style", "line": int, "description": "..."}],
    "score": int,
    "summary": "..."
}"""
    }
]

# 或者用OpenAI的response_format参数
response = await client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    response_format={"type": "json_object"},
)
`

---

## 第三部分：Function Calling（工具调用）

### 3.1 工具定义

`python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "在互联网上搜索信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 5,
                    }
                },
                "required": ["query"],
            }
        }
    }
]
`

### 3.2 Tool Use循环

`python
import json

async def agent_loop(user_input: str):
    messages = [{"role": "user", "content": user_input}]
    
    while True:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        
        msg = response.choices[0].message
        
        # 如果模型没有调用工具，返回最终回答
        if not msg.tool_calls:
            return msg.content
        
        # 处理工具调用
        messages.append(msg)  # 把assistant的tool_call消息加入
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            # 执行工具
            result = await execute_tool(func_name, **func_args)
            
            # 把工具结果加回消息
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })
    
    # 继续循环，让模型基于工具结果生成回答
`

### 3.3 多工具协作

`python
tools = [
    # 搜索工具
    {"type": "function", "function": {
        "name": "web_search",
        "description": "搜索网络获取实时信息",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string"}
        }, "required": ["query"]}
    }},
    # 计算工具
    {"type": "function", "function": {
        "name": "calculate",
        "description": "执行数学计算",
        "parameters": {"type": "object", "properties": {
            "expression": {"type": "string", "description": "数学表达式"}
        }, "required": ["expression"]}
    }},
    # 文件操作工具
    {"type": "function", "function": {
        "name": "file_operation",
        "description": "读写文件",
        "parameters": {"type": "object", "properties": {
            "action": {"type": "string", "enum": ["read", "write", "list"]},
            "path": {"type": "string"},
            "content": {"type": "string"},
        }, "required": ["action", "path"]}
    }},
]
`

---

## 第四部分：Memory系统

### 4.1 对话历史管理

最基础的Memory就是保留所有消息，但有token限制：

`python
class ConversationMemory:
    def __init__(self, system_prompt: str, max_tokens: int = 4000):
        self.messages: list[dict] = [
            {"role": "system", "content": system_prompt}
        ]
        self.max_tokens = max_tokens
    
    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> list[dict]:
        """返回当前消息，确保不超过token限制"""
        total = self._count_tokens()
        while total > self.max_tokens and len(self.messages) > 2:
            # 移除最早的消息（保留system prompt）
            removed = self.messages.pop(1)
            total -= self._estimate_tokens(removed["content"])
        return self.messages
    
    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 3  # 粗略估计
`

### 4.2 摘要压缩

当对话太长时，用AI压缩历史：

`python
class SummaryMemory:
    def __init__(self, client: AsyncOpenAI, max_messages: int = 20):
        self.client = client
        self.summary = ""
        self.recent_messages: list[dict] = []
        self.max_messages = max_messages
    
    def add(self, role: str, content: str):
        self.recent_messages.append({"role": role, "content": content})
    
    async def compress(self):
        """当消息过多时，压缩历史为摘要"""
        if len(self.recent_messages) > self.max_messages:
            old = self.recent_messages[:self.max_messages // 2]
            self.recent_messages = self.recent_messages[self.max_messages // 2:]
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "请将以下对话压缩为简洁摘要："},
                    *old,
                ],
            )
            self.summary = response.choices[0].message.content
    
    def get_messages(self) -> list[dict]:
        messages = []
        if self.summary:
            messages.append({
                "role": "system", 
                "content": f"之前对话摘要：{self.summary}"
            })
        messages.extend(self.recent_messages)
        return messages
`

### 4.3 向量记忆基础

用embedding存储和检索相关记忆：

`python
import numpy as np

class VectorMemory:
    def __init__(self):
        self.memories: list[dict] = []  # {text, embedding, metadata}
    
    async def add(self, text: str, client: AsyncOpenAI):
        """添加一条记忆"""
        resp = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        embedding = resp.data[0].embedding
        self.memories.append({"text": text, "embedding": embedding})
    
    async def search(self, query: str, client: AsyncOpenAI, top_k: int = 5) -> list[str]:
        """搜索相关记忆"""
        resp = await client.embeddings.create(
            model="text-embedding-3-small",
            input=query,
        )
        query_emb = np.array(resp.data[0].embedding)
        
        scored = []
        for mem in self.memories:
            sim = np.dot(query_emb, np.array(mem["embedding"]))
            scored.append((sim, mem["text"]))
        
        scored.sort(reverse=True)
        return [text for _, text in scored[:top_k]]
`

---

## 第五部分：Agent架构

### 5.1 ReAct模式

ReAct = Reasoning + Acting。模型交替思考和行动：

`
Thought: 用户问的是天气，我需要调用天气API
Action: call_weather_api(city="北京")
Observation: 北京今天晴，28°C
Thought: 我已经获取了天气信息，可以回答了
Answer: 北京今天天气晴朗，气温28°C。
`

### 5.2 Agent核心循环

`python
class Agent:
    def __init__(self, engine: AIEngine, tools: ToolRegistry, memory: Memory):
        self.engine = engine
        self.tools = tools
        self.memory = memory
        self.max_iterations = 10
    
    async def run(self, user_input: str) -> str:
        self.memory.add("user", user_input)
        
        for i in range(self.max_iterations):
            messages = self.memory.get_messages()
            tool_defs = self.tools.get_definitions()
            
            response = await self.engine.chat(messages, tools=tool_defs)
            
            if response.tool_calls:
                # 模型要求调用工具
                self.memory.add("assistant", response)
                
                for call in response.tool_calls:
                    result = await self.tools.execute(
                        call.function.name,
                        **json.loads(call.function.arguments)
                    )
                    self.memory.add_tool_result(call.id, str(result))
            else:
                # 模型给出最终回答
                answer = response.content
                self.memory.add("assistant", answer)
                return answer
        
        return "达到最大迭代次数，未能完成任务。"
`

### 5.3 Tool Registry（工具注册器）

`python
from typing import Callable, Any

class Tool:
    def __init__(self, name: str, description: str, parameters: dict, func: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.func = func
    
    def to_openai_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def register(self, name: str, description: str, parameters: dict):
        """装饰器：注册一个工具"""
        def decorator(func: Callable) -> Callable:
            self._tools[name] = Tool(name, description, parameters, func)
            return func
        return decorator
    
    async def execute(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            return f"错误：未知工具 {name}"
        return await self._tools[name].func(**kwargs)
    
    def get_definitions(self) -> list[dict]:
        return [tool.to_openai_format() for tool in self._tools.values()]
`

### 5.4 异步Agent设计

为什么Agent必须异步：
- API调用是IO密集型，同步会阻塞
- 工具执行可能并发（搜索+计算同时进行）
- 流式输出需要异步迭代

`python
import asyncio

class AsyncAgent:
    async def run_parallel_tools(self, tool_calls: list) -> list[dict]:
        """并行执行多个工具调用"""
        tasks = []
        for call in tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)
            tasks.append(self.tools.execute(name, **args))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            {"tool_call_id": call.id, "content": str(r) if not isinstance(r, Exception) else f"错误: {r}"}
            for call, r in zip(tool_calls, results)
        ]
`

---

## 第六部分：设计模式在AI应用中的应用

### 6.1 策略模式（Strategy）

不同的Memory策略可以互换：

`python
class MemoryStrategy(ABC):
    @abstractmethod
    def get_messages(self) -> list[dict]: ...
    @abstractmethod
    def add(self, role: str, content: str): ...

class SlidingWindowMemory(MemoryStrategy): ...
class SummaryMemory(MemoryStrategy): ...
class VectorMemory(MemoryStrategy): ...

# Agent使用策略
class Agent:
    def __init__(self, memory_strategy: MemoryStrategy):
        self.memory = memory_strategy
`

### 6.2 观察者模式（Observer）

监控Agent的每一步操作：

`python
class AgentObserver:
    def on_tool_call(self, tool_name: str, args: dict): ...
    def on_response(self, content: str): ...
    def on_error(self, error: Exception): ...

class ObservableAgent:
    def __init__(self):
        self.observers: list[AgentObserver] = []
    
    def add_observer(self, observer: AgentObserver):
        self.observers.append(observer)
    
    def _notify(self, event: str, **data):
        for obs in self.observers:
            getattr(obs, f"on_{event}")(**data)
`

### 6.3 注册器模式（Registry）

`python
# 用装饰器自动注册工具
registry = ToolRegistry()

@registry.register(
    name="calculator",
    description="计算数学表达式",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string"}
        },
        "required": ["expression"]
    }
)
async def calculator(expression: str) -> str:
    return str(eval(expression))  # 生产环境用ast.literal_eval或专用库
`

---

## 关键要点总结

| 概念 | 核心 | 常见坑 |
|------|------|--------|
| Chat Completion | messages列表，role区分角色 | 忘记system prompt |
| Temperature | 0=确定，1=随机 | 代码生成用低temperature |
| Function Calling | 定义tools→模型决策→执行→返回结果 | tool_call_id必须匹配 |
| Memory | 控制上下文长度 | 别把所有消息都塞进去 |
| Agent Loop | Think→Act→Observe循环 | 必须有最大迭代限制 |
| 异步 | API调用和工具执行都用async | 别忘了gather并行 |

## 📝 预习检查

在开始挑战之前，确保你能回答：
1. Chat Completion API的messages列表中，system/user/assistant/tool各自的作用？
2. Function Calling的完整流程是什么？
3. 为什么Agent需要最大迭代限制？
4. 摘要压缩和向量检索分别适合什么场景？
