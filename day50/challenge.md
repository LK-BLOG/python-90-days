# Day 50 挑战任务

## Challenge 1: 项目骨架 + 数据模型
**目标：** 搭建博客API项目结构

**要求：**
1. 创建项目结构（FastAPI标准布局）
2. SQLAlchemy模型（User/Article/Comment/Tag）
3. Alembic迁移配置
4. 数据库连接（async SQLite）
5. Pydantic schemas

**验收：** 迁移成功，能创建表
**难度：** ⭐⭐

---

## Challenge 2: CRUD路由
**目标：** 实现文章和评论的增删改查

**要求：**
1. 文章CRUD（list/create/read/update/delete）
2. 评论CRUD
3. 标签关联
4. 返回正确的HTTP状态码
5. 输入验证（Pydantic schema）

**验收：** 所有CRUD操作通过测试
**难度：** ⭐⭐

---

## Challenge 3: 分页和过滤
**目标：** API支持分页和条件过滤

**要求：**
1. Offset分页（page/page_size）
2. 游标分页
3. 按标签过滤
4. 按作者过滤
5. 按时间排序

**验收：** 分页和过滤参数正确生效
**难度：** ⭐⭐

---

## Challenge 4: 用户认证 + 权限
**目标：** JWT认证和权限控制

**要求：**
1. 用户注册（密码哈希）
2. 用户登录（JWT token）
3. 依赖注入获取当前用户
4. 只有作者能编辑/删除自己的文章
5. 未认证用户只能读

**验收：** 非作者不能删除他人文章
**难度：** ⭐⭐⭐
