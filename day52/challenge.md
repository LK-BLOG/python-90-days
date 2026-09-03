# Day 52 挑战任务

## Challenge 1: OpenAPI文档完善
**目标：** 让API文档完整清晰

**要求：**
1. 所有路由有summary和description
2. response_model定义
3. 错误响应定义
4. 标签分组
5. 示例数据

**验收：** /docs页面完整可用
**难度：** ⭐

---

## Challenge 2: 查询优化
**目标：** 消除N+1问题

**要求：**
1. 使用selectinload优化关联查询
2. 添加数据库索引
3. 实现分页游标
4. 用EXPLAIN分析慢查询

**验收：** 列表接口<100ms
**难度：** ⭐⭐

---

## Challenge 3: 安全加固
**目标：** 加固API安全

**要求：**
1. 安全响应头
2. CORS严格配置
3. 输入验证（防XSS）
4. 速率限制
5. SQL注入防护

**验收：** 通过基本安全检查
**难度：** ⭐⭐

---

## Challenge 4: Docker + CI/CD
**目标：** 部署博客API

**要求：**
1. Dockerfile（多阶段构建）
2. docker-compose.yml
3. GitHub Actions CI（测试+lint）
4. CD（部署到服务器）

**验收：** docker-compose up能启动完整服务
**难度：** ⭐⭐⭐
