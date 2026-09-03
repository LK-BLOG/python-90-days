# Day 48 挑战任务

## Challenge 1: .env + 环境变量
**目标：** 使用dotenv加载配置

**要求：**
1. 创建.env文件（含DB_URL/SECRET_KEY/DEBUG）
2. 用python-dotenv加载
3. 支持.env.local覆盖
4. 测试验证优先级

**验收：** 环境变量>默认值, .env.local>.env
**难度：** ⭐

---

## Challenge 2: Pydantic Settings验证
**目标：** 类型安全的配置

**要求：**
1. 定义Settings类（至少8个字段）
2. 包含验证器（端口范围/URL格式/日志级别）
3. 支持嵌套配置
4. 从环境变量读取（带前缀）
5. 测试验证所有验证器

**验收：** 非法配置启动时报错
**难度：** ⭐⭐

---

## Challenge 3: 多环境切换
**目标：** 不同环境不同配置

**要求：**
1. 创建DevSettings/ProdSettings/TestSettings
2. 通过APP_ENV环境变量切换
3. 每个环境有不同的默认值
4. 测试验证环境切换

**验收：** 改APP_ENV即可切换整个配置
**难度：** ⭐⭐

---

## Challenge 4: 配置热更新
**目标：** 运行时更新配置

**要求：**
1. 实现ConfigManager类
2. 监控配置文件变化
3. 变化时触发回调
4. 支持手动reload
5. 线程安全

**验收：** 修改配置文件后服务自动更新
**难度：** ⭐⭐⭐
