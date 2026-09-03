# Day 84: 挑战练习

## 挑战说明

通过 5 个递进式挑战，掌握权限系统的核心实现。每个挑战对应一个具体的权限场景。

### Challenge 01: 基础权限对象
**目标**：实现 Permission 和 Role 数据类，支持权限的创建、比较和角色的权限集合管理。
- 实现 `Permission.__eq__` 和 `__hash__`
- 实现 `Role.add_permission()` 和 `Role.remove_permission()`
- 实现 `Role.has_permission()`（考虑 MANAGE 级别包含子操作）

### Challenge 02: RBAC 引擎
**目标**：实现完整的 RBAC 引擎。
- `add_role(role)` / `remove_role(name)`
- `assign_role(user, role)` / `revoke_role(user, role)`
- `check_permission(user, resource, action)` → bool
- `get_user_permissions(user)` → Set[Permission]

### Challenge 03: 权限装饰器
**目标**：实现 `@require` 装饰器，支持单个权限和多个权限（OR 关系）检查。
- `@require(resource, action)` 单权限
- `@require_any(resource1=action1, resource2=action2)` 多权限
- 装饰器在权限不足时抛出 `PermissionDenied` 异常并记录日志

### Challenge 04: 权限继承
**目标**：实现角色继承（Role Hierarchy）。
- 角色可以继承另一个角色的所有权限
- `Role("editor", parent=readers)` → editor 自动拥有 reader 的权限
- 多级继承不产生循环（检测循环依赖）
- `get_effective_permissions(role)` 返回含继承的全部权限

### Challenge 05: 策略引擎
**目标**：实现简单的 ABAC 策略引擎，作为 RBAC 的补充。
- 策略格式：`if user.department == "engineering" and resource.classification <= "internal" then allow`
- `PolicyRule` 类支持条件表达式评估
- 策略优先级排序（显式 deny > allow > 默认 deny）

### 运行测试
```bash
python -m pytest tests/test_permission.py -v
```
