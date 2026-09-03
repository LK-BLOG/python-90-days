# Day 81: Context Engineering

## 1. 上下文窗口管理

### 1.1 为什么 Context Engineering 很重要？

LLM 的上下文窗口是有限的。Context Engineering 就是在有限空间里塞进最有价值的信息：

`
总上下文窗口 = System Prompt + 历史对话 + 当前查询 + 工具结果 + 输出预留
`

如果超过窗口限制，旧的信息会被截断。管理不好就：
- 关键信息被丢弃
- Agent 忘记之前的决定
- 工具调用结果被截断

### 1.2 Token 计数器

`python
import tiktoken
from typing import List, Dict


class TokenCounter:
    \"\"\"Token 计数和管理\"\"\"
    
    def __init__(self, model: str = "gpt-4"):
        try:
            self.enc = tiktoken.encoding_for_model(model)
        except KeyError:
            self.enc = tiktoken.get_encoding("cl100k_base")
    
    def count(self, text: str) -> int:
        return len(self.enc.encode(text))
    
    def count_messages(self, messages: List[Dict]) -> int:
        total = 0
        for msg in messages:
            total += self.count(msg.get("content", ""))
            total += 4  # 每条消息的格式开销
        return total
    
    def fit_to_budget(self, messages: List[Dict], budget: int) -> List[Dict]:
        \"\"\"将消息列表裁剪到 token 预算内\"\"\"
        # 保留 system prompt 和最后一条消息
        if len(messages) <= 2:
            return messages
        
        system = messages[0]
        query = messages[-1]
        history = messages[1:-1]
        
        system_tokens = self.count_messages([system])
        query_tokens = self.count_messages([query])
        remaining = budget - system_tokens - query_tokens - 100  # 100 token 余量
        
        # 从最新的消息开始保留
        kept = []
        used = 0
        for msg in reversed(history):
            msg_tokens = self.count_messages([msg])
            if used + msg_tokens > remaining:
                break
            kept.insert(0, msg)
            used += msg_tokens
        
        return [system] + kept + [query]
`

## 2. 上下文压缩与摘要

`python
class ContextCompressor:
    \"\"\"上下文压缩器\"\"\"
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
    
    def compress_history(self, messages: List[Dict], llm=None) -> List[Dict]:
        \"\"\"压缩对话历史\"\"\"
        if not messages:
            return messages
        
        # 策略1: 保留最近N条
        if len(messages) > 10:
            recent = messages[-5:]
            old = messages[:-5]
            
            # 将旧消息摘要
            summary = self._summarize(old, llm)
            
            return [
                {"role": "system", "content": f"对话历史摘要: {summary}"}
            ] + recent
        
        return messages
    
    def _summarize(self, messages: List[Dict], llm=None) -> str:
        \"\"\"摘要旧消息\"\"\"
        # 模拟摘要
        topics = set()
        for msg in messages:
            content = msg.get("content", "")
            if "搜索" in content:
                topics.add("信息搜索")
            if "代码" in content:
                topics.add("代码编写")
            if "分析" in content:
                topics.add("数据分析")
        
        return "之前的对话涉及: " + ", ".join(topics) if topics else "无重要信息"
    
    def extract_key_info(self, messages: List[Dict]) -> Dict:
        \"\"\"从消息中提取关键信息\"\"\"
        key_info = {
            "user_goal": "",
            "decisions_made": [],
            "tools_used": [],
            "errors": [],
        }
        
        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "")
            
            if role == "user" and not key_info["user_goal"]:
                key_info["user_goal"] = content[:100]
            
            if "Tool:" in content:
                tool_name = content.split("Tool:")[1].split("\n")[0].strip()
                if tool_name not in key_info["tools_used"]:
                    key_info["tools_used"].append(tool_name)
            
            if "错误" in content or "Error" in content:
                key_info["errors"].append(content[:100])
        
        return key_info
`

## 3. 动态 Prompt 注入

`python
class DynamicPromptBuilder:
    \"\"\"动态构建 System Prompt\"\"\"
    
    def __init__(self):
        self.base_prompt = "你是一个智能助手。"
        self.sections = {}
        self.priority_order = ["tools", "context", "constraints", "examples"]
    
    def add_section(self, name: str, content: str, priority: int = 0):
        self.sections[name] = {"content": content, "priority": priority}
    
    def build(self, token_budget: int = 4000) -> str:
        \"\"\"在 token 预算内构建最优 prompt\"\"\"
        sections = sorted(
            self.sections.items(),
            key=lambda x: x[1]["priority"],
            reverse=True
        )
        
        prompt = self.base_prompt
        used_tokens = len(prompt) // 4  # 粗略估计
        
        for name, info in sections:
            section_text = f"\n\n## {name}\n{info['content']}"
            section_tokens = len(section_text) // 4
            
            if used_tokens + section_tokens < token_budget - 200:  # 预留输出
                prompt += section_text
                used_tokens += section_tokens
            else:
                # 尝试截断
                remaining_tokens = token_budget - used_tokens - 200
                if remaining_tokens > 50:
                    truncated = info['content'][:remaining_tokens * 4]
                    prompt += f"\n\n## {name} (部分)\n{truncated}..."
                    break
        
        return prompt
    
    def inject_dynamic_context(self, task: str, available_tools: list) -> str:
        \"\"\"根据当前任务动态注入上下文\"\"\"
        context = self.base_prompt
        
        # 只注入相关的工具描述
        relevant_tools = [t for t in available_tools if self._is_relevant(t, task)]
        if relevant_tools:
            tool_desc = "\n".join([
                f"- {t['name']}: {t['description']}"
                for t in relevant_tools[:5]  # 限制工具数量
            ])
            context += f"\n\n可用工具:\n{tool_desc}"
        
        return context
    
    def _is_relevant(self, tool: dict, task: str) -> bool:
        # 简单相关性检查
        task_lower = task.lower()
        return any(kw in task_lower for kw in tool['name'].lower().split('_'))
`

## 4. System Prompt 工程

`python
class SystemPromptEngineer:
    \"\"\"System Prompt 工程器\"\"\"
    
    @staticmethod
    def build_agent_prompt(
        role: str,
        tools: list,
        constraints: list = None,
        examples: list = None
    ) -> str:
        \"\"\"构建 Agent 的 System Prompt\"\"\"
        prompt = f"""# 角色
你是一个{role}。

# 能力
"""
        
        # 工具描述
        if tools:
            prompt += "你可以使用以下工具:\n"
            for t in tools:
                prompt += f"- **{t['name']}**: {t['description']}\n"
                if 'params' in t:
                    prompt += f"  参数: {t['params']}\n"
        
        # 约束
        if constraints:
            prompt += "\n# 约束\n"
            for c in constraints:
                prompt += f"- {c}\n"
        
        # 示例
        if examples:
            prompt += "\n# 示例\n"
            for i, ex in enumerate(examples):
                prompt += f"\n## 示例 {i+1}\n"
                prompt += f"用户: {ex['input']}\n"
                prompt += f"助手: {ex['output']}\n"
        
        # 输出格式
        prompt += """
# 输出格式
每次行动前，先输出你的思考（Thought），然后执行行动（Action）。
格式:
Thought: [你的分析]
Action: [工具名](参数)
"""
        
        return prompt
    
    @staticmethod
    def optimize_for_task(prompt: str, task_type: str) -> str:
        \"\"\"针对特定任务类型优化 prompt\"\"\"
        optimizations = {
            "coding": "重点: 代码质量、错误处理、类型安全",
            "analysis": "重点: 数据准确性、逻辑严谨、结论有据",
            "creative": "重点: 原创性、多样性、用户偏好",
        }
        
        if task_type in optimizations:
            prompt += f"\n\n# 任务重点\n{optimizations[task_type]}"
        
        return prompt
`

## 5. 上下文窗口策略

`python
class ContextWindowStrategy:
    \"\"\"上下文窗口管理策略\"\"\"
    
    STRATEGIES = {
        "sliding_window": "滑动窗口 - 只保留最近N条",
        "summarize_old": "摘要旧消息 - 压缩历史",
        "keep_important": "重要性过滤 - 只保留关键信息",
        "hierarchical": "层次化 - 按重要性分层保留",
    }
    
    def __init__(self, strategy: str = "sliding_window", max_messages: int = 20):
        self.strategy = strategy
        self.max_messages = max_messages
    
    def apply(self, messages: list) -> list:
        if self.strategy == "sliding_window":
            return self._sliding_window(messages)
        elif self.strategy == "summarize_old":
            return self._summarize_old(messages)
        elif self.strategy == "keep_important":
            return self._keep_important(messages)
        return messages
    
    def _sliding_window(self, messages: list) -> list:
        if len(messages) <= self.max_messages:
            return messages
        return messages[-self.max_messages:]
    
    def _summarize_old(self, messages: list) -> list:
        if len(messages) <= 10:
            return messages
        old = messages[:-5]
        recent = messages[-5:]
        summary = f"之前{len(old)}轮对话的摘要: 讨论了{len(old)}个话题"
        return [{"role": "system", "content": summary}] + recent
    
    def _keep_important(self, messages: list) -> list:
        important = [m for m in messages if m.get("role") == "user" or "Tool:" in m.get("content", "")]
        if len(important) > self.max_messages:
            return important[-self.max_messages:]
        return important
`

## 6. 常见错误

1. **System Prompt 太长**：占了大半窗口 → 精简，只保留必要信息
2. **不压缩历史**：对话越来越长直到溢出 → 定期摘要
3. **工具描述重复**：同一工具描述出现多次 → 去重
4. **信息优先级错误**：关键信息被截断 → 高优先级放前面
5. **没有 Token 预算**：不知道还能塞多少 → 用 TokenCounter 监控

## 7. 动手练习

### 练习 1：实现 Token 计数器
### 练习 2：实现上下文压缩器
### 练习 3：实现动态 Prompt 构建器
