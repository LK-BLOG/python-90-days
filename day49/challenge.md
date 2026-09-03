# Day 49 挑战任务

## Challenge 1: 内存缓存实现
**目标：** 实现一个TTL内存缓存

**要求：**
1. 实现MemoryCache类（get/set/delete）
2. 支持TTL过期
3. 支持maxsize淘汰（LRU）
4. 支持cache_info统计
5. 线程安全

**验收：** get/set/TTL/LRU全部正常
**难度：** ⭐⭐

---

## Challenge 2: Redis缓存集成
**目标：** 用Redis实现缓存层

**要求：**
1. 实现RedisCache类
2. JSON序列化/反序列化
3. 支持TTL
4. 批量操作（mget/mset）
5. 写测试（可用fakeredis）

**验收：** 能正确存取数据
**难度：** ⭐⭐

---

## Challenge 3: 缓存失效策略
**目标：** 解决缓存问题

**要求：**
1. 实现空值缓存（防穿透）
2. TTL加随机偏移（防雪崩）
3. 实现SingleFlight（防击穿）
4. 写测试验证每个策略

**验收：** 三种问题都有对应的解决方案
**难度：** ⭐⭐⭐

---

## Challenge 4: 多级缓存
**目标：** 实现L1+L2多级缓存

**要求：**
1. L1: 进程内TTL缓存
2. L2: Redis缓存
3. 读取顺序: L1 → L2
4. 写入同时更新L1和L2
5. L1 miss自动从L2加载
6. 支持主动失效

**验收：** L1命中率高，L2作为fallback
**难度：** ⭐⭐⭐
