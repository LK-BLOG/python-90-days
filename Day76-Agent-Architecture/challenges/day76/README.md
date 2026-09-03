# Day 76 挑战任务

## 任务：实现ReAct Agent

### 要求

1. 完成ase_agent.py中的ReActAgent类
2. 实现_think方法：调用LLM决定下一步行动
3. 实现un方法：执行思考-行动循环
4. 记录每个步骤的执行轨迹

### 测试

运行测试确保实现正确：
`ash
python -m pytest tests/test_agent.py -v
`

### 扩展

1. 添加更多工具
2. 实现错误处理
3. 优化提示词
