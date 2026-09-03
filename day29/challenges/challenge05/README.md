# Challenge 5: 多工具Agent

## 目标
构建一个完整的ReAct Agent，整合Memory + Tools + AI Engine。

## 要求
1. 组合Memory + Tools + AI Engine
2. 实现ReAct循环（Thought→Act→Observe）
3. 支持并行工具调用（asyncio.gather）
4. 最大迭代次数限制
5. 每一步都有日志输出

## 验收
- [ ] Agent能完成实际任务
- [ ] 并行工具调用工作
- [ ] 有日志输出
- [ ] 最大迭代限制生效
