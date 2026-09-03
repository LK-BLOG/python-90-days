# Day 64: Function Calling

## 1. 工作流程
用户输入 -> LLM判断需要工具 -> 返回tool_calls -> 应用执行 -> 结果发回LLM

## 2. 工具定义
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]
```

## 3. 调用流程
```python
response = client.chat.completions.create(..., tools=tools, tool_choice="auto")
if response.choices[0].message.tool_calls:
    for tc in response.choices[0].message.tool_calls:
        result = execute(tc.function.name, tc.function.arguments)
```

## 4. 并行调用
LLM可一次返回多个tool_calls，并行执行后一起返回。
