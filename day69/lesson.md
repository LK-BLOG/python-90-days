# Day 69: AI 应用架构

## 1. 设计模式
- Prompt-Response: 最简单, 单次调用
- Chain: 多步管道串联
- Agent: 自主决策 + 工具调用
- RAG: 检索增强

## 2. 流式输出
SSE(Server-Sent Events) 或 WebSocket 实现逐token推送, 提升用户体验。

## 3. 异步调用
asyncio + semaphore 控制并发, 大幅提升吞吐量。

## 4. 可靠性三板斧
- 速率限制: 令牌桶/滑动窗口
- 重试: 指数退避 + 抖动
- 降级: 小模型兜底 / 缓存响应

## 5. 成本控制
Prompt压缩 | 响应缓存 | 智能模型选择 | 预算告警
