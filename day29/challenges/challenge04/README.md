# Challenge 4: Memory系统

## 目标
实现对话记忆管理，支持滑动窗口和摘要压缩。

## 要求
1. 实现滑动窗口Memory（保留最近N条消息）
2. 实现Token感知Memory（根据token数限制）
3. System prompt始终保留
4. 对外提供统一接口

## 验收
- [ ] 滑动窗口正确工作
- [ ] Token限制有效
- [ ] System prompt不被移除
- [ ] clear()正确清空
