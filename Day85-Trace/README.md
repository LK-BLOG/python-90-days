# Day 85: Trace (执行追踪系统)

## 学习目标
- 理解分布式追踪的核心概念（Span/Trace/Context）
- 实现 Agent 调用链追踪系统
- 掌握 Token 计数与成本追踪
- 学会日志聚合与性能分析

## 核心概念
1. **Trace**：一次完整的请求/执行过程
2. **Span**：Trace 中的单个操作单元，有开始/结束时间
3. **Context Propagation**：跨函数/服务传递追踪上下文
4. **Token 成本**：大模型调用的 token 用量与费用追踪

## 文件结构
```
Day85-Trace/
├── README.md
├── lesson.md
├── challenge.md
├── ultimate_challenge.md
├── examples/
│   ├── 01_span_trace.py
│   ├── 02_context_propagation.py
│   └── 03_cost_tracker.py
├── starter/
│   └── trace_system.py
├── tests/
│   └── test_trace.py
└── challenges/
    └── day85/
        ├── challenge01-05/
        └── ultimate/
```

## 预计学习时间
- 课程阅读：2 小时
- 示例实践：1.5 小时
- 挑战练习：2-3 小时
- 终极挑战：3-4 小时
