# Challenge 05: 通用 LLM 客户端

## Boss 挑战

前 4 个挑战分别实现了 Token 计数、多轮对话、参数调优和流式输出。现在你要把它们**全部整合**，构建一个生产级的通用 LLM 客户端。

## 目标

实现 `LLMClient` 类，支持：
- 统一的 `.chat()` / `.stream()` / `.batch()` 接口
- 内置 Token 计数与预算控制
- 多轮对话历史管理（自动截断 + 摘要）
- 参数配置（temperature / top_p / max_tokens）
- 请求重试与超时处理
- Token 用量统计与成本估算

## 验收标准
- [ ] `.chat(messages)` 返回完整回复 + usage 统计
- [ ] `.stream(messages)` 逐 token 输出
- [ ] `.batch([msgs1, msgs2, ...])` 并发批量调用
- [ ] 对话历史自动截断，不超过 max_tokens 预算
- [ ] 请求失败时指数退避重试
- [ ] `client.stats` 返回总 token 用量和估算费用
- [ ] 通过 test_day61.py 全部测试
