# Day 89: Runtime Implementation

## 1. Agent Loop

`python
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentState(Enum):
    IDLE = 'idle'
    THINKING = 'thinking'
    ACTING = 'acting'
    OBSERVING = 'observing'
    FINISHED = 'finished'
    ERROR = 'error'

@dataclass
class Message:
    role: str
    content: str
    metadata: Optional[Dict] = None

class AgentLoop:
    def __init__(self, llm_client, tool_executor, memory, state_manager):
        self.llm = llm_client
        self.tools = tool_executor
        self.memory = memory
        self.state = state_manager
        self.max_iterations = 10
        self.current_state = AgentState.IDLE
    
    async def run(self, user_input: str) -> str:
        self.memory.add_message(Message(role='user', content=user_input))
        
        for i in range(self.max_iterations):
            self.current_state = AgentState.THINKING
            response = await self.llm.chat(self.memory.get_messages())
            
            if response.tool_calls:
                self.current_state = AgentState.ACTING
                tool_results = await self.tools.execute(response.tool_calls)
                
                for result in tool_results:
                    self.memory.add_message(Message(
                        role='tool',
                        content=str(result),
                        metadata={'tool': result.tool_name}
                    ))
                
                self.current_state = AgentState.OBSERVING
            else:
                self.memory.add_message(Message(
                    role='assistant',
                    content=response.content
                ))
                self.current_state = AgentState.FINISHED
                return response.content
        
        raise RuntimeError('max iterations reached')
`

## 2. Tool Execution Engine

`python
from typing import Callable, Any, Dict
import inspect
import asyncio

class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = self._extract_parameters()
    
    def _extract_parameters(self) -> Dict:
        sig = inspect.signature(self.func)
        params = {}
        for name, param in sig.parameters.items():
            params[name] = {
                'type': param.annotation.__name__ if param.annotation != inspect.Parameter.empty else 'any',
                'required': param.default == inspect.Parameter.empty,
                'default': param.default if param.default != inspect.Parameter.empty else None
            }
        return params
    
    async def execute(self, **kwargs) -> Any:
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        return self.func(**kwargs)

class ToolExecutor:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, name: str = None, description: str = ''):
        def decorator(func: Callable):
            tool_name = name or func.__name__
            self.tools[tool_name] = Tool(tool_name, func, description)
            return func
        return decorator
    
    async def execute(self, tool_calls: List[Dict]) -> List[Any]:
        results = []
        for call in tool_calls:
            tool_name = call['name']
            args = call.get('arguments', {})
            if tool_name not in self.tools:
                raise ValueError(f'tool not found: {tool_name}')
            tool = self.tools[tool_name]
            result = await tool.execute(**args)
            results.append({'tool': tool_name, 'result': result, 'success': True})
        return results
`

## 3. Memory + State

`python
from collections import deque
from datetime import datetime

class MemoryManager:
    def __init__(self, max_messages: int = 100):
        self.messages: deque = deque(maxlen=max_messages)
        self.summaries: List[str] = []
    
    def add_message(self, message: Message):
        message.metadata = message.metadata or {}
        message.metadata['timestamp'] = datetime.now().isoformat()
        self.messages.append(message)
    
    def get_messages(self, limit: int = None) -> List[Message]:
        if limit:
            return list(self.messages)[-limit:]
        return list(self.messages)
    
    def summarize_and_compress(self):
        if len(self.messages) < 50:
            return
        old_messages = list(self.messages)[:40]
        summary = self._generate_summary(old_messages)
        self.summaries.append(summary)
        for _ in range(40):
            self.messages.popleft()
    
    def _generate_summary(self, messages: List[Message]) -> str:
        return f'summary ({len(messages)} messages)'

class StateManager:
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.history: List[Dict] = []
    
    def set(self, key: str, value: Any):
        self.history.append({
            'action': 'set',
            'key': key,
            'old_value': self.state.get(key),
            'new_value': value,
            'timestamp': datetime.now().isoformat()
        })
        self.state[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)
    
    def snapshot(self) -> Dict:
        return self.state.copy()
`

## 4. Sandbox + Permission

`python
import subprocess
from typing import Set

class Sandbox:
    def __init__(self):
        self.allowed_commands: Set[str] = {'python', 'pip', 'ls', 'cat'}
        self.max_execution_time = 30
    
    def validate_command(self, command: str) -> bool:
        parts = command.split()
        if not parts:
            return False
        cmd = parts[0]
        if cmd not in self.allowed_commands:
            return False
        dangerous_flags = ['-exec', '|', ';', '&&']
        for flag in dangerous_flags:
            if flag in command:
                return False
        return True
    
    def execute(self, command: str) -> Dict:
        if not self.validate_command(command):
            raise PermissionError(f'blocked: {command}')
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=self.max_execution_time)
        return {'success': result.returncode == 0, 'stdout': result.stdout, 'stderr': result.stderr}

from enum import Enum
from functools import wraps

class Permission(Enum):
    READ = 'read'
    WRITE = 'write'
    EXECUTE = 'execute'
    NETWORK = 'network'

class PermissionManager:
    def __init__(self):
        self.permissions: Dict[str, Set[Permission]] = {}
        self.audit_log: List[Dict] = []
    
    def grant(self, role: str, permission: Permission):
        if role not in self.permissions:
            self.permissions[role] = set()
        self.permissions[role].add(permission)
    
    def check(self, role: str, permission: Permission) -> bool:
        granted = permission in self.permissions.get(role, set())
        self.audit_log.append({'role': role, 'permission': permission.value, 'granted': granted})
        return granted
`

## 5. Trace System

`python
import uuid
import time
from contextlib import contextmanager
from typing import Generator

@dataclass
class TraceSpan:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = None
    status: str = 'OK'
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
    
    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return 0
        return (self.end_time - self.start_time) * 1000

class Tracer:
    def __init__(self):
        self.spans: List[TraceSpan] = []
        self.current_trace_id: Optional[str] = None
    
    def start_trace(self, name: str) -> str:
        trace_id = str(uuid.uuid4())
        self.current_trace_id = trace_id
        span = TraceSpan(trace_id=trace_id, span_id=str(uuid.uuid4()), parent_span_id=None, name=name, start_time=time.time())
        self.spans.append(span)
        return trace_id
    
    @contextmanager
    def span(self, name: str, parent_id: str = None) -> Generator[TraceSpan, None, None]:
        span = TraceSpan(trace_id=self.current_trace_id or str(uuid.uuid4()), span_id=str(uuid.uuid4()), parent_span_id=parent_id, name=name, start_time=time.time())
        self.spans.append(span)
        try:
            yield span
            span.status = 'OK'
        except Exception as e:
            span.status = f'ERROR: {str(e)}'
            span.attributes['error'] = str(e)
            raise
        finally:
            span.end_time = time.time()
    
    def export(self, trace_id: str) -> Dict:
        spans = [s for s in self.spans if s.trace_id == trace_id]
        return {
            'trace_id': trace_id,
            'spans': [{'span_id': s.span_id, 'name': s.name, 'duration_ms': s.duration_ms, 'status': s.status} for s in spans]
        }
`

## 6. Error Handling

`python
import asyncio
from functools import wraps
import random

def retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        jitter = random.uniform(0, 0.1) * current_delay
                        await asyncio.sleep(current_delay + jitter)
                        current_delay *= backoff
            raise last_exception
        return wrapper
    return decorator
`

## 7. Complete Runtime

`python
class AgentRuntime:
    def __init__(self, config: Dict):
        self.config = config
        self.memory = MemoryManager(config.get('max_messages', 100))
        self.state = StateManager()
        self.tools = ToolExecutor()
        self.sandbox = Sandbox()
        self.permissions = PermissionManager()
        self.tracer = Tracer()
        self.error_handler = ErrorHandler(self.tracer)
        self.loop = AgentLoop(
            llm_client=self._create_llm_client(),
            tool_executor=self.tools,
            memory=self.memory,
            state_manager=self.state
        )
    
    async def process(self, user_input: str) -> str:
        with self.tracer.span('process_request') as span:
            span.attributes['user_input'] = user_input[:100]
            result = await self.loop.run(user_input)
            span.attributes['result_length'] = len(result)
            return result
    
    def get_metrics(self) -> Dict:
        return {
            'total_requests': len(self.memory.messages),
            'total_spans': len(self.tracer.spans),
            'state_size': len(self.state.state),
            'registered_tools': len(self.tools.tools)
        }
`

## Summary
- Agent Loop: think-act-observe cycle
- Tool Executor: safe tool invocation
- Memory + State: history and state management
- Sandbox + Permission: security isolation
- Trace: execution tracking
- Error Handling: retry and recovery
