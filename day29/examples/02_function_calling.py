"""Day 29 示例2：Function Calling + Agent循环"""

import json
import asyncio
from openai import AsyncOpenAI

# ======== 工具定义 ========

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "列出目录内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "目录路径"}
                },
                "required": ["path"]
            }
        }
    }
]


# ======== 工具执行 ========

def calculator(expression: str) -> str:
    """安全计算数学表达式"""
    import ast
    try:
        # 只允许安全的数学操作
        tree = ast.parse(expression, mode='eval')
        result = eval(compile(tree, '<calc>', 'eval'))
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"

def read_file(path: str) -> str:
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content) > 5000:
            return content[:5000] + f"\n... (截断，共{len(content)}字符)"
        return content
    except Exception as e:
        return f"读取错误: {e}"

def list_directory(path: str) -> str:
    """列出目录内容"""
    import os
    try:
        items = os.listdir(path)
        return "\n".join(items[:50])  # 最多返回50项
    except Exception as e:
        return f"列出错误: {e}"

TOOL_MAP = {
    "calculator": calculator,
    "read_file": read_file,
    "list_directory": list_directory,
}


# ======== Agent循环 ========

async def agent_loop(user_input: str, api_key: str):
    """完整的Agent循环：对话 → 工具调用 → 继续对话"""
    client = AsyncOpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": "你是一个有用的AI助手。你需要使用工具来回答用户的问题。"},
        {"role": "user", "content": user_input},
    ]
    
    max_iterations = 5
    
    for i in range(max_iterations):
        print(f"\n--- 迭代 {i + 1} ---")
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
        )
        
        msg = response.choices[0].message
        
        # 没有工具调用，返回最终回答
        if not msg.tool_calls:
            print(f"最终回答: {msg.content}")
            return msg.content
        
        # 有工具调用
        messages.append(msg)  # assistant消息（含tool_calls）
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            print(f"调用工具: {func_name}({func_args})")
            
            # 执行工具
            func = TOOL_MAP.get(func_name)
            if func:
                result = func(**func_args)
            else:
                result = f"未知工具: {func_name}"
            
            print(f"工具结果: {result}")
            
            # 添加工具结果到消息
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })
    
    return "达到最大迭代次数"


if __name__ == "__main__":
    # asyncio.run(agent_loop("计算 (3+5)*12 的结果", "your-api-key"))
    print("示例代码，请设置API Key后运行")
