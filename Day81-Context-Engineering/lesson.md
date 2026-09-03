# Day 81 课程：Context Engineering

## 1. 上下文窗口管理

`python
from dataclasses import dataclass
from typing import Any
import tiktoken


@dataclass
class ContextWindow:
    '''上下文窗口'''
    max_tokens: int = 4096
    system_tokens: int = 0
    memory_tokens: int = 0
    history_tokens: int = 0
    current_tokens: int = 0
    response_tokens: int = 0
    
    @property
    def used_tokens(self) -> int:
        '''已使用的token数'''
        return (
            self.system_tokens + 
            self.memory_tokens + 
            self.history_tokens + 
            self.current_tokens
        )
    
    @property
    def available_tokens(self) -> int:
        '''可用的token数'''
        return self.max_tokens - self.used_tokens - self.response_tokens
    
    def can_fit(self, tokens: int) -> bool:
        '''检查是否能放入'''
        return tokens <= self.available_tokens
    
    def allocate_response(self, tokens: int):
        '''分配响应空间'''
        if tokens > self.available_tokens:
            raise ValueError("响应空间不足")
        self.response_tokens = tokens


class ContextManager:
    '''上下文管理器'''
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.window = ContextWindow(max_tokens=max_tokens)
        self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        '''计算token数'''
        return len(self.encoder.encode(text))
    
    def build_context(
        self,
        system_prompt: str,
        memory: list[str],
        history: list[dict],
        current_input: str,
        reserve_response: int = 1000
    ) -> dict:
        '''构建上下文'''
        # 计算各部分token数
        system_tokens = self.count_tokens(system_prompt)
        memory_tokens = sum(self.count_tokens(m) for m in memory)
        
        # 为响应预留空间
        self.window.allocate_response(reserve_response)
        
        # 计算历史可用空间
        available_for_history = self.window.available_tokens - self.count_tokens(current_input)
        
        # 截断历史
        truncated_history = self._truncate_history(history, available_for_history)
        history_tokens = sum(
            self.count_tokens(str(msg)) for msg in truncated_history
        )
        
        # 更新窗口状态
        self.window.system_tokens = system_tokens
        self.window.memory_tokens = memory_tokens
        self.window.history_tokens = history_tokens
        self.window.current_tokens = self.count_tokens(current_input)
        
        return {
            "system": system_prompt,
            "memory": memory,
            "history": truncated_history,
            "current": current_input,
            "stats": {
                "total_tokens": self.window.used_tokens + self.window.response_tokens,
                "available": self.window.available_tokens
            }
        }
    
    def _truncate_history(self, history: list[dict], max_tokens: int) -> list[dict]:
        '''截断历史记录'''
        if not history:
            return []
        
        truncated = []
        current_tokens = 0
        
        # 从最新的开始，保留最新的对话
        for msg in reversed(history):
            msg_tokens = self.count_tokens(str(msg))
            if current_tokens + msg_tokens > max_tokens:
                break
            truncated.insert(0, msg)
            current_tokens += msg_tokens
        
        return truncated
`

## 2. 上下文压缩与摘要

`python
class ContextCompressor:
    '''上下文压缩器'''
    
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        '''生成摘要'''
        if self.llm_provider:
            prompt = f"请将以下内容压缩为{max_length}字以内的摘要：\n\n{text}"
            return self.llm_provider(prompt)
        
        # 简单的截断摘要
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    def extract_key_points(self, text: str, max_points: int = 5) -> list[str]:
        '''提取关键点'''
        # 简单的关键词提取
        sentences = text.split('。')
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and len(key_points) < max_points:
                key_points.append(sentence)
        
        return key_points
    
    def compress_history(self, history: list[dict], target_tokens: int) -> list[dict]:
        '''压缩对话历史'''
        encoder = tiktoken.get_encoding("cl100k_base")
        
        # 计算当前token数
        current_tokens = sum(
            len(encoder.encode(str(msg))) for msg in history
        )
        
        if current_tokens <= target_tokens:
            return history
        
        # 压缩策略：
        # 1. 保留最近的对话
        # 2. 摘要化早期对话
        
        compressed = []
        recent_messages = history[-5:]  # 保留最近5条
        early_messages = history[:-5]
        
        # 摘要化早期对话
        if early_messages:
            early_text = "\n".join([str(msg) for msg in early_messages])
            summary = self.summarize(early_text, 200)
            compressed.append({
                "role": "system",
                "content": f"早期对话摘要: {summary}"
            })
        
        compressed.extend(recent_messages)
        
        return compressed
`

## 3. 动态上下文注入

`python
from typing import Callable


class DynamicContextInjector:
    '''动态上下文注入器'''
    
    def __init__(self):
        self.injections: list[Callable] = []
        self.context_cache: dict[str, Any] = {}
    
    def register(self, name: str, provider: Callable):
        '''注册上下文提供者'''
        self.injections.append({
            "name": name,
            "provider": provider
        })
    
    def inject(self, base_context: dict, query: str) -> dict:
        '''注入动态上下文'''
        enhanced_context = base_context.copy()
        
        for injection in self.injections:
            try:
                name = injection["name"]
                provider = injection["provider"]
                
                # 获取动态上下文
                dynamic_content = provider(query)
                
                if dynamic_content:
                    if "dynamic_context" not in enhanced_context:
                        enhanced_context["dynamic_context"] = {}
                    enhanced_context["dynamic_context"][name] = dynamic_content
            
            except Exception as e:
                print(f"注入 {name} 失败: {e}")
        
        return enhanced_context
    
    def clear_cache(self):
        '''清除缓存'''
        self.context_cache.clear()


# 示例：时间上下文注入
def time_context_provider(query: str) -> str:
    '''时间上下文提供者'''
    from datetime import datetime
    now = datetime.now()
    return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"


# 示例：用户画像注入
def user_profile_provider(query: str) -> dict:
    '''用户画像提供者'''
    # 这里可以从数据库或缓存获取
    return {
        "name": "用户",
        "preferences": ["Python", "AI"],
        "history_summary": "之前询问过Python相关问题"
    }
`

## 4. System Prompt工程

`python
class SystemPromptBuilder:
    '''系统提示构建器'''
    
    def __init__(self):
        self.sections: list[dict] = []
    
    def add_section(self, name: str, content: str, priority: int = 0):
        '''添加section'''
        self.sections.append({
            "name": name,
            "content": content,
            "priority": priority
        })
    
    def build(self, max_tokens: int = 2000) -> str:
        '''构建系统提示'''
        # 按优先级排序
        sorted_sections = sorted(
            self.sections, 
            key=lambda x: x["priority"], 
            reverse=True
        )
        
        encoder = tiktoken.get_encoding("cl100k_base")
        
        # 构建提示，控制token数
        parts = []
        current_tokens = 0
        
        for section in sorted_sections:
            section_tokens = len(encoder.encode(section["content"]))
            
            if current_tokens + section_tokens > max_tokens:
                # 截断这个section
                remaining_tokens = max_tokens - current_tokens
                truncated = self._truncate_to_tokens(
                    section["content"], remaining_tokens
                )
                parts.append(f"[{section['name']}]\n{truncated}")
                break
            
            parts.append(f"[{section['name']}]\n{section['content']}")
            current_tokens += section_tokens
        
        return "\n\n".join(parts)
    
    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        '''截断到指定token数'''
        encoder = tiktoken.get_encoding("cl100k_base")
        tokens = encoder.encode(text)
        
        if len(tokens) <= max_tokens:
            return text
        
        truncated_tokens = tokens[:max_tokens]
        return encoder.decode(truncated_tokens) + "..."


# 预定义的System Prompt模板
class PromptTemplates:
    '''提示模板'''
    
    RESEARCHAssistant = """你是一个研究助手。你的职责是：
1. 准确回答用户的问题
2. 引用可靠的来源
3. 承认不确定的地方
4. 提供进一步学习的建议"""

    CODINGAssistant = """你是一个编程助手。你的职责是：
1. 编写清晰、高效的代码
2. 解释代码逻辑
3. 提供最佳实践建议
4. 帮助调试和解决问题"""
    
    TASK_PLANNER = """你是一个任务规划助手。你的职责是：
1. 分解复杂任务
2. 制定执行计划
3. 识别依赖关系
4. 提供时间估算"""
`

## 5. 上下文预算控制

`python
class ContextBudget:
    '''上下文预算'''
    
    def __init__(self, total_budget: int = 4096):
        self.total_budget = total_budget
        self.allocations: dict[str, int] = {}
        self.used: dict[str, int] = {}
    
    def allocate(self, category: str, tokens: int):
        '''分配预算'''
        if sum(self.allocations.values()) + tokens > self.total_budget:
            raise ValueError("预算不足")
        self.allocations[category] = tokens
        self.used[category] = 0
    
    def consume(self, category: str, tokens: int) -> bool:
        '''消耗预算'''
        if category not in self.allocations:
            return False
        
        if self.used[category] + tokens > self.allocations[category]:
            return False
        
        self.used[category] += tokens
        return True
    
    def available(self, category: str) -> int:
        '''获取可用预算'''
        return self.allocations.get(category, 0) - self.used.get(category, 0)
    
    def status(self) -> dict:
        '''获取预算状态'''
        return {
            "total": self.total_budget,
            "allocated": self.allocations,
            "used": self.used,
            "available": {
                cat: self.available(cat) 
                for cat in self.allocations
            }
        }
`

## 6. 本日总结

- ContextManager管理上下文窗口
- ContextCompressor压缩和摘要化上下文
- DynamicContextInjector动态注入上下文
- SystemPromptBuilder构建优化的系统提示
- ContextBudget控制上下文预算

明天我们将学习Memory系统。
