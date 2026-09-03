# Day 76 - 挑战 1: ReAct Agent 循环
## 难度: ⭐⭐

## 任务
实现一个完整的 ReAct Agent 循环，支持多个工具调用。

## 要求
1. 实现 ReActAgent 类，包含 un() 方法
2. 支持 Thought → Action → Observation 循环
3. 解析 LLM 输出，提取 Thought 和 Action
4. 支持 inish action 退出循环
5. 设置 max_steps 防止无限循环

## 工具要求
至少实现以下工具：
- calculator(expression): 数学计算
- search(query): 模拟搜索
- lookup(term): 术语查询

## 验证
运行测试：python -m pytest tests/test_challenge1.py -v
"@ | Out-File -Encoding utf8 "D:\Python-Learn-30-days\challenges\day76\challenge01\README.md"

@"
\"\"\"挑战1: ReAct Agent 测试\"\"\"
import sys
sys.path.insert(0, '../../../day76/starter')

def test_basic_react_loop():
    \"\"\"测试基本 ReAct 循环能正常执行并退出\"\"\"
    # TODO: 从 starter 代码导入并测试
    from react_agent import Tool, ReActAgent
    
    tools = [
        Tool("calc", "计算", lambda expression="": str(eval(expression))),
    ]
    agent = ReActAgent(tools)
    result = agent.run("1+1等于几")
    assert result is not None
    print("✅ basic_react_loop 通过")

def test_max_steps_enforced():
    \"\"\"测试最大步数限制\"\"\"
    from react_agent import Tool, ReActAgent
    tools = [Tool("noop", "空", lambda: "ok")]
    agent = ReActAgent(tools, max_steps=2)
    assert agent.max_steps == 2
    print("✅ max_steps 通过")

if __name__ == "__main__":
    test_basic_react_loop()
    test_max_steps_enforced()
