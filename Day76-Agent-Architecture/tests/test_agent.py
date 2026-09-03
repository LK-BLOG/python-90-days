'''
Day 76 测试：Agent架构测试
'''

import pytest
from starter.base_agent import (
    ReActAgent, PlanAndExecuteAgent, 
    BaseTool, AgentResult
)


class MockTool(BaseTool):
    '''模拟工具'''
    
    def __init__(self, name: str = "mock", response: str = "mock result"):
        super().__init__(name, f"模拟工具: {name}")
        self.response = response
        self.call_count = 0
        self.last_input = None
    
    def execute(self, input_data: str) -> str:
        self.call_count += 1
        self.last_input = input_data
        return self.response


class MockLLM:
    '''模拟LLM'''
    
    def __init__(self, responses: list[dict] = None):
        self.responses = responses or []
        self.call_count = 0
    
    def __call__(self, prompt: str) -> str:
        import json
        if self.call_count < len(self.responses):
            response = self.responses[self.call_count]
        else:
            response = {"thought": "思考", "answer": "默认回答"}
        self.call_count += 1
        return json.dumps(response)


class TestBaseTool:
    '''测试工具基类'''
    
    def test_tool_creation(self):
        '''测试工具创建'''
        tool = MockTool("test", "test result")
        assert tool.name == "test"
        assert tool.description == "模拟工具: test"
    
    def test_tool_execution(self):
        '''测试工具执行'''
        tool = MockTool("test", "result")
        result = tool.execute("input")
        assert result == "result"
        assert tool.call_count == 1
        assert tool.last_input == "input"


class TestReActAgent:
    '''测试ReAct Agent'''
    
    def test_agent_creation(self):
        '''测试Agent创建'''
        agent = ReActAgent()
        assert agent.tools == {}
        assert agent.steps == []
    
    def test_register_tool(self):
        '''测试工具注册'''
        agent = ReActAgent()
        tool = MockTool("search", "search result")
        agent.register_tool(tool)
        assert "search" in agent.tools
    
    def test_simple_query(self):
        '''测试简单查询'''
        # 模拟LLM返回最终答案
        mock_llm = MockLLM([
            {"thought": "这是简单问题", "answer": "Python是一种编程语言"}
        ])
        
        agent = ReActAgent(llm_provider=mock_llm)
        result = agent.run("什么是Python？")
        
        assert result.success is True
        assert "Python" in result.answer
        assert result.total_steps == 1


class TestPlanAndExecuteAgent:
    '''测试Plan-and-Execute Agent'''
    
    def test_agent_creation(self):
        '''测试Agent创建'''
        agent = PlanAndExecuteAgent()
        assert agent.tools == {}
    
    def test_plan_creation(self):
        '''测试计划创建'''
        # TODO: 实现测试
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
