'''
Day 76 挑战起步代码
'''

from starter.base_agent import ReActAgent, MockTool

# 创建Agent
agent = ReActAgent()

# 注册工具
agent.register_tool(MockTool("search", "搜索结果"))

# 测试运行
result = agent.run("什么是Python？")
print(f"回答: {result.answer}")
