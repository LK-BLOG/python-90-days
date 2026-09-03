\"\"\"Day 76 测试\"\"\"
import sys
sys.path.insert(0, '../starter')
from react_agent import Tool, ReActAgent


def test_tool_creation():
    \"\"\"测试工具创建\"\"\"
    tool = Tool("test", "测试工具", lambda x="": f"result:{x}")
    assert tool.name == "test"
    assert tool.description == "测试工具"
    assert tool.execute(x="hello") == "result:hello"
    print("✅ test_tool_creation 通过")


def test_tool_error_handling():
    \"\"\"测试工具错误处理\"\"\"
    def bad_func():
        raise ValueError("boom")
    tool = Tool("bad", "会出错的工具", bad_func)
    result = tool.execute()
    assert "错误" in result or "boom" in result
    print("✅ test_tool_error_handling 通过")


def test_agent_max_steps():
    \"\"\"测试最大步数限制\"\"\"
    tools = [Tool("noop", "空工具", lambda: "ok")]
    agent = ReActAgent(tools, max_steps=3)
    # 确保不会无限循环
    assert agent.max_steps == 3
    print("✅ test_agent_max_steps 通过")


def test_parse_response():
    \"\"\"测试响应解析\"\"\"
    agent = ReActAgent([])
    response = "Thought: 我需要计算\nAction: calc(expression=1+1)"
    result = agent.parse_response(response)
    assert result is not None
    print("✅ test_parse_response 通过")


if __name__ == "__main__":
    test_tool_creation()
    test_tool_error_handling()
    test_agent_max_steps()
    test_parse_response()
    print("\n所有测试通过！")
