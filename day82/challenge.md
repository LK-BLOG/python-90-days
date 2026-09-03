# Day 82: 挑战概览

## Challenge 1: 实现Agent状态机（⭐⭐）
设计一个Agent状态机，支持以下状态：
- IDLE、PLANNING、EXECUTING、WAITING、DONE、ERROR
- 至少5种合法转换路径
- 支持进入/退出回调
- 记录完整状态转换历史

**要求**：编写`AgentStateMachine`类和测试。

## Challenge 2: 文件状态持久化（⭐⭐）
实现基于文件的Agent状态持久化系统：
- 原子写入（先写临时文件再重命名）
- 支持save/load/list/delete操作
- 处理并发写入冲突
- 支持状态过期清理

## Challenge 3: 断点续传Agent（⭐⭐⭐）
构建一个支持断点续传的Agent：
- 每个处理步骤自动保存Checkpoint
- 崩溃后从最近的Checkpoint恢复
- 支持列出所有Checkpoint
- 支持清理旧Checkpoint保留最近N个

## Challenge 4: 状态序列化器（⭐⭐⭐）
实现带版本迁移的状态序列化：
- 注册版本迁移函数
- 自动检测版本并逐级迁移
- 处理自定义类型（datetime/set等）
- 保证向前兼容

## Challenge 5: 带锁的分布式状态管理（⭐⭐⭐⭐）
实现支持并发安全的状态管理：
- 乐观锁（version字段）
- 状态冲突检测
- 冲突解决策略（last-write-wins / merge）
- 支持字段级更新

## Ultimate Challenge: 完整Agent状态管理系统（⭐⭐⭐⭐⭐）
综合以上所有组件，构建一个生产级的Agent状态管理系统，详见 [ultimate_challenge.md](./ultimate_challenge.md)。
