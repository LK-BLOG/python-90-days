# Day 30 课程：项目架构设计指南

## 第一部分：架构设计思路

### 1.1 为什么需要架构

单文件脚本能跑，但不能维护。当你有200行代码时，一个文件没问题；当你有2000行代码时，没有架构就是灾难。

架构的本质是**分治**：把复杂系统拆成小模块，每个模块只负责一件事。

### 1.2 分层设计

`
┌─────────────────────────────────┐
│          CLI层 (用户交互)         │  ← 人在这里
├─────────────────────────────────┤
│        Agent层 (决策中心)         │  ← 大脑在这里
├─────────────────────────────────┤
│   Engine层    │    Tool层        │  ← 手脚在这里
│  (AI调用)     │   (工具执行)      │
├──────────────┴──────────────────┤
│     Memory层    │   Config层     │  ← 记忆和配置
├─────────────────┴───────────────┤
│           Utils层 (工具函数)       │  ← 基础设施
└─────────────────────────────────┘
`

每一层只依赖它下面的层，不跨层调用。

### 1.3 核心设计原则

**SOLID原则在AI助手中的应用：**

- **S** (单一职责): ngine.py 只负责API调用，memory.py 只负责记忆，	ools/registry.py 只负责工具注册
- **O** (开闭): 通过注册器模式，新增工具不需要修改任何已有代码
- **L** (里氏替换): 所有Memory实现都遵循 BaseMemory 接口，可互换使用
- **I** (接口隔离): BaseMemory 和 ToolRegistry 是独立接口，不需要的不要依赖
- **D** (依赖倒置): Agent 依赖 AIEngine 和 ToolRegistry 的抽象，不依赖具体实现

---

## 第二部分：模块设计详解

### 2.1 Core模块 — Agent核心

**agent.py — 决策中心**

Agent是整个系统的大脑，负责协调所有模块：

`python
class Agent:
    def __init__(
        self,
        engine: AIEngine,
        tools: ToolRegistry,
        memory: BaseMemory,
        config: Config,
    ):
        self.engine = engine
        self.tools = tools
        self.memory = memory
        self.config = config
        self.max_iterations = config.max_iterations  # 默认10
    
    async def run(self, user_input: str) -> AsyncGenerator[str, None]:
        """Agent主循环 — ReAct模式"""
        self.memory.add("user", user_input)
        
        for i in range(self.max_iterations):
            messages = self.memory.get_messages()
            tool_defs = self.tools.get_definitions()
            
            response = await self.engine.chat(messages, tools=tool_defs)
            
            if response.tool_calls:
                # Yield思考过程
                yield f"[思考] 需要使用工具...\n"
                
                self.memory.add("assistant", response.raw_message)
                
                # 并行执行工具
                results = await self._execute_parallel(response.tool_calls)
                
                for result in results:
                    self.memory.add("tool", result["content"])
                    yield f"[工具] {result['tool_name']}: {result['content'][:100]}\n"
            else:
                # 最终回答
                self.memory.add("assistant", response.content)
                yield response.content
                return
        
        yield "达到最大迭代次数，任务未能完成。"
`

**engine.py — AI引擎**

封装所有API调用逻辑：

`python
class AIEngine:
    def __init__(self, config: Config):
        self.client = AsyncOpenAI(api_key=config.api_key)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
    
    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> ChatResponse:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
        
        response = await self.client.chat.completions.create(**kwargs)
        return self._parse_response(response)
    
    async def chat_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
`

**prompt.py — Prompt管理**

`python
class PromptManager:
    def __init__(self, system_prompt: str = ""):
        self.system_prompt = system_prompt
        self.templates: dict[str, str] = {}
    
    def register(self, name: str, template: str):
        self.templates[name] = template
    
    def render(self, name: str, **kwargs) -> str:
        return self.templates[name].format(**kwargs)
    
    def get_system_message(self) -> dict:
        return {"role": "system", "content": self.system_prompt}
`

### 2.2 Tools模块 — 工具系统

**设计模式：注册器模式 + 策略模式**

**base.py — 工具基类**

`python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    content: str
    error: str | None = None

class BaseTool(ABC):
    """所有工具的基类"""
    
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @property
    @abstractmethod
    def description(self) -> str: ...
    
    @property
    @abstractmethod
    def parameters(self) -> dict: ...
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult: ...
    
    def to_openai_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }
`

**registry.py — 工具注册器**

`python
class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool) -> BaseTool:
        """注册一个工具实例"""
        self._tools[tool.name] = tool
        return tool
    
    def register_class(self, cls: type[BaseTool]) -> type[BaseTool]:
        """注册一个工具类（装饰器）"""
        instance = cls()
        self._tools[instance.name] = instance
        return cls
    
    async def execute(self, name: str, **kwargs) -> ToolResult:
        if name not in self._tools:
            return ToolResult(success=False, content="", error=f"未知工具: {name}")
        try:
            return await self._tools[name].execute(**kwargs)
        except Exception as e:
            return ToolResult(success=False, content="", error=str(e))
    
    def get_definitions(self) -> list[dict]:
        return [tool.to_openai_format() for tool in self._tools.values()]
`

**具体工具实现示例 — file_tool.py**

`python
class FileReadTool(BaseTool):
    name = "file_read"
    description = "读取文件内容"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "encoding": {"type": "string", "default": "utf-8"},
        },
        "required": ["path"],
    }
    
    async def execute(self, path: str, encoding: str = "utf-8") -> ToolResult:
        try:
            # 安全检查
            path = Path(path).resolve()
            if not path.exists():
                return ToolResult(False, "", f"文件不存在: {path}")
            
            content = path.read_text(encoding=encoding)
            if len(content) > 10000:
                content = content[:10000] + f"\n... (截断，共{len(content)}字符)"
            
            return ToolResult(True, content)
        except Exception as e:
            return ToolResult(False, "", str(e))
`

### 2.3 Memory模块 — 记忆系统

**设计模式：策略模式**

`python
# base.py
class BaseMemory(ABC):
    @abstractmethod
    def add(self, role: str, content: str) -> None: ...
    
    @abstractmethod
    def get_messages(self) -> list[dict]: ...
    
    @abstractmethod
    def clear(self) -> None: ...
    
    @abstractmethod
    def get_token_count(self) -> int: ...

# history.py — 对话历史
class HistoryMemory(BaseMemory):
    """最简单的滑动窗口记忆"""
    ...

# summary.py — 摘要压缩记忆
class SummaryMemory(BaseMemory):
    """带AI压缩的记忆"""
    ...
`

**Agent如何使用策略模式：**

`python
# 不同场景用不同的Memory策略
agent_simple = Agent(memory=SlidingWindowMemory(max_messages=10))
agent_smart = Agent(memory=SummaryMemory(engine=engine, max_recent=20))
agent_token = Agent(memory=TokenAwareMemory(max_tokens=4000))
`

### 2.4 Config模块 — 配置管理

**设计模式：单例 + 环境变量优先**

`python
from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    """配置：环境变量 > 配置文件 > 默认值"""
    
    api_key: str = Field(default="", description="OpenAI API Key")
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    max_iterations: int = 10
    memory_max_tokens: int = 4000
    log_level: str = "INFO"
    
    model_config = {
        "env_prefix": "AI_ASSISTANT_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

# 单例
_config: Config | None = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config
`

### 2.5 CLI模块 — 命令行界面

`python
class CLI:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.commands: dict[str, Callable] = {
            "/quit": self._cmd_quit,
            "/clear": self._cmd_clear,
            "/history": self._cmd_history,
            "/tools": self._cmd_tools,
        }
    
    async def run(self):
        print("AI Assistant 已启动。输入 /quit 退出。")
        
        while True:
            try:
                user_input = input("\n你: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            
            if not user_input:
                continue
            
            if user_input.startswith("/"):
                await self._handle_command(user_input)
                continue
            
            async for chunk in self.agent.run(user_input):
                print(chunk, end="", flush=True)
            print()
`

---

## 第三部分：异步编程在Agent中的应用

### 3.1 为什么Agent必须异步

1. **API调用是IO密集型**：一个请求可能需要2-10秒，同步会阻塞整个程序
2. **工具可能并发执行**：搜索和计算可以同时进行
3. **流式输出**：需要异步迭代器逐字输出

### 3.2 关键异步模式

`python
# 1. 并行工具执行
results = await asyncio.gather(*[
    self.tools.execute(name, **args)
    for name, args in tool_calls
])

# 2. 流式输出
async def stream_response(self, user_input: str):
    async for chunk in self.engine.chat_stream(messages):
        yield chunk

# 3. 超时控制
try:
    result = await asyncio.wait_for(
        self.tools.execute("web_search", query=query),
        timeout=10.0,
    )
except asyncio.TimeoutError:
    result = ToolResult(False, "", "工具执行超时")
`

---

## 第四部分：设计模式总结

| 模式 | 在项目中的应用 | 好处 |
|------|-------------|------|
| **策略模式** | Memory可互换（滑动窗口/摘要/向量） | 运行时切换记忆策略 |
| **注册器模式** | 工具自动注册 | 新增工具零修改 |
| **观察者模式** | 日志/监控Agent每一步 | 解耦日志和核心逻辑 |
| **模板方法** | BaseTool定义接口 | 所有工具行为一致 |
| **工厂模式** | 从配置创建Agent | 配置驱动构建 |
| **单例模式** | Config全局唯一 | 统一配置访问 |
| **上下文管理器** | 资源管理（API客户端、文件句柄） | 自动清理资源 |

---

## 第五部分：代码组织最佳实践

### 5.1 __init__.py 的作用

`python
# src/ai_assistant/__init__.py
"""AI Assistant - 一个功能完整的AI命令行助手"""
__version__ = "1.0.0"

# 导出核心类，方便外部使用
from ai_assistant.core.agent import Agent
from ai_assistant.config.settings import Config

__all__ = ["Agent", "Config"]
`

### 5.2 __main__.py 的作用

`python
# src/ai_assistant/__main__.py
"""允许 python -m ai_assistant 启动"""
import asyncio
from ai_assistant.cli import CLI

def main():
    asyncio.run(CLI().run())

if __name__ == "__main__":
    main()
`

### 5.3 类型注解规范

`python
# 所有公开方法都要有类型注解
async def run(self, user_input: str) -> AsyncGenerator[str, None]:
    ...

def add(self, role: str, content: str) -> None:
    ...

# 使用类型别名提高可读性
from typing import TypeAlias
MessageList: TypeAlias = list[dict[str, str]]
`

### 5.4 上下文管理器管理资源

`python
class AISession:
    """AI会话上下文管理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client: AsyncOpenAI | None = None
    
    async def __aenter__(self):
        self.client = AsyncOpenAI(api_key=self.config.api_key)
        return self
    
    async def __aexit__(self, *exc):
        if self.client:
            await self.client.close()

# 使用
async with AISession(config) as session:
    response = await session.client.chat.completions.create(...)
`

---

## 第六部分：测试策略

### 6.1 测试层次

`
tests/
├── test_config.py     # 配置加载测试
├── test_tools.py      # 工具执行测试（用mock）
├── test_memory.py     # 记忆系统测试
├── test_agent.py      # Agent逻辑测试（mock API）
└── conftest.py        # 共享fixtures
`

### 6.2 Mock策略

`python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_engine():
    engine = AsyncMock()
    engine.chat.return_value = ChatResponse(
        content="测试回复",
        tool_calls=None,
    )
    return engine

@pytest.fixture
def agent(mock_engine, tool_registry, sliding_memory):
    return Agent(engine=mock_engine, tools=tool_registry, memory=sliding_memory)

async def test_agent_responds(agent):
    result = await agent.run("你好")
    assert result == "测试回复"
`

---

## 验收检查清单

在提交之前，用这个清单检查你的项目：

- [ ] python -m ai_assistant 可以启动
- [ ] 多轮对话正常工作
- [ ] 至少4个工具可用
- [ ] Memory管理对话历史
- [ ] 配置从环境变量/文件读取
- [ ] 所有模块有类型注解
- [ ] pytest tests/ 通过
- [ ] 不是单文件——真正的包结构
- [ ] pyproject.toml配置正确
- [ ] 代码可读，有适当注释
