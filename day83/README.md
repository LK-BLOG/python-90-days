# Day 83: Sandbox — 代码执行沙箱

> 把代码丢进沙箱跑，炸了也不心疼。

## 今日目标
- 理解代码执行沙箱的核心设计（subprocess/受限exec）
- 掌握文件系统隔离与虚拟文件系统
- 实现网络访问控制与资源限制（CPU/内存/时间）
- 构建超时控制与强制终止机制
- 设计安全的代码执行环境

## 前置知识
- Day 81-82: Agent工具调用, Agent State

## 目录结构
```
day83/
├── README.md          # 本文件
├── lesson.md          # 完整知识点
├── challenge.md       # 5个挑战概览
├── ultimate_challenge.md  # 终极挑战
├── examples/          # 5个示例
├── starter/           # 3个骨架
├── tests/             # 3个测试
└── code/              # 你的代码
```

## 学习路线
1. 先读 `lesson.md` 掌握理论
2. 运行 `examples/` 理解实现
3. 完成 `starter/` + `tests/` 验证
4. 挑战 `challenge.md` 的5个任务
5. 终极挑战：完整沙箱系统

## 核心思想
沙箱的本质是**不信任**。你不信任用户代码，所以隔离它、限制它、监控它。安全的代价是性能和灵活性，但这是必须的。
