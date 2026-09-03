# Day 84: 终极挑战 - 完整的 Agent 权限网关

## 目标

构建一个生产级的 Agent 工具调用权限网关，整合 Day 84 所有知识点。

## 需求

### 1. 工具注册与权限绑定

```python
# 注册工具时绑定权限
registry = SecureToolRegistry(rbac_engine)

@registry.tool(
    name="read_file",
    permission=Permission("file", Action.READ),
    description="读取文件内容",
    rate_limit=100,  # 每分钟最多100次
)
def read_file(path: str) -> str: ...
```

### 2. 多层权限检查

```
请求 → IP白名单 → 用户认证 → RBAC权限 → ABAC策略 → 速率限制 → 执行 → 审计
```

每层失败都返回具体错误和建议。

### 3. 实时权限刷新

支持权限配置的热更新，无需重启服务：

```python
watcher = PermissionWatcher("rbac_config.json")
watcher.on_change(lambda new_config: rbac_engine.reload(new_config))
watcher.start()  # 后台监控配置变化
```

### 4. 权限审计仪表盘

```python
class AuditDashboard:
    def summary(self, hours: int = 24) -> dict:
        """返回最近N小时的审计统计"""

    def user_activity(self, username: str) -> list:
        """指定用户的操作历史"""

    def security_alerts(self) -> list:
        """异常检测：频繁被拒绝的操作、异常时间访问等"""
```

### 5. 权限模板系统

预设角色模板，快速初始化：

```python
templates = PermissionTemplates()
templates.list()  # ["reader", "editor", "admin", "tool_executor"]
admin_role = templates.create_role("admin")  # 带预设权限
```

## 验收标准

1. [ ] 工具调用必须经过完整权限检查链
2. [ ] 支持 RBAC + ABAC 混合策略
3. [ ] 审计日志完整可查，支持按用户/时间/资源过滤
4. [ ] 权限配置热更新，不中断服务
5. [ ] 所有测试通过：`python -m pytest tests/ -v`
6. [ ] 支持至少 3 种预设角色模板

## 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 架构设计 | 25% | 分层清晰，扩展性好 |
| 权限逻辑 | 25% | RBAC/ABAC实现正确 |
| 审计系统 | 20% | 日志完整，查询灵活 |
| 错误处理 | 15% | 异常清晰，失败安全 |
| 代码质量 | 15% | 类型标注，文档完善 |
