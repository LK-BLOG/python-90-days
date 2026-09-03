# Day 76 挑战任务

## 挑战 1：实现 ReAct Agent 循环
**难度：⭐⭐**

实现一个 ReAct Agent，能够：
1. 接收用户查询
2. 交替进行 Thought 和 Action
3. 使用工具获取 Observation
4. 在得到最终答案时退出

### 要求
- 实现 ReActAgent 类
- 至少支持 3 个工具（calculator、search、lookup）
- 解析 LLM 输出中的 Thought/Action/Observation
- 设置最大步数限制

## 挑战 2：实现工具注册系统
**难度：⭐⭐**

实现一个工具注册表：
1. 工具可以被注册和发现
2. 根据工具名查找并执行
3. 生成工具描述供 LLM 使用

## 挑战 3：实现 Plan-and-Execute
**难度：⭐⭐⭐**

实现先规划再执行的 Agent：
1. create_plan() 方法生成步骤列表
2. xecute_step() 方法执行每个步骤
3. 支持 eplan() 在失败时重新规划
4. 汇总所有步骤结果

## 挑战 4：Agent 循环可视化
**难度：⭐⭐⭐**

给 Agent 循环添加追踪能力：
1. 记录每一步的 Thought/Action/Observation
2. 计算每步耗时和 token 用量
3. 生成执行报告

## 挑战 5（Boss）：混合模式 Agent
**难度：⭐⭐⭐⭐⭐**

实现一个结合 ReAct 和 Plan-and-Execute 的混合 Agent：
1. 先用 Plan-and-Execute 制定大计划
2. 每个步骤内部用 ReAct 执行
3. 步骤失败时触发重新规划
4. 完整的状态管理和错误恢复
