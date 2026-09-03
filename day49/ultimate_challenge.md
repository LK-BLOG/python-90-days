# Day 49 终极挑战：API多级缓存系统

## 🏆 Boss Challenge

为一个API系统实现完整的多级缓存策略。

## 功能需求

### P0 — 必须完成
- [ ] 内存L1缓存（LRU + TTL）
- [ ] Redis L2缓存
- [ ] 多级缓存读写
- [ ] Cache-Aside模式
- [ ] 空值缓存防穿透

### P1 — 应该完成
- [ ] TTL随机偏移防雪崩
- [ ] SingleFlight防击穿
- [ ] 缓存预热
- [ ] 缓存统计（命中率/miss率）

### P2 — 加分项
- [ ] 缓存标签（tag-based失效）
- [ ] 写回模式（Write-Behind）
- [ ] 缓存监控dashboard

## 验收标准
1. 读请求90%+命中L1
2. L2作为二级fallback
3. 不存在的数据不会穿透到DB
4. 热点key不会击穿
