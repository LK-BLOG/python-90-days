# Day 77 测试
import sys
sys.path.insert(0, '../starter')
from tool_system import ToolResult, BaseTool, ToolRegistry, CalculatorTool


def test_tool_result():
    r = ToolResult(success=True, data="42")
    assert r.success
    assert r.data == "42"
    r2 = ToolResult(success=False, error="boom")
    assert not r2.success
    print("✅ ToolResult 通过")


def test_base_tool_run():
    calc = CalculatorTool()
    result = calc.run(expression="2+2")
    assert result.success
    assert result.data == "4"
    print("✅ BaseTool.run 通过")


def test_registry():
    registry = ToolRegistry()
    calc = CalculatorTool()
    registry.register(calc)
    assert "calculator" in registry.list_all()
    print("✅ ToolRegistry 通过")


if __name__ == "__main__":
    test_tool_result()
    test_base_tool_run()
    test_registry()
    print("\n所有测试通过！")
