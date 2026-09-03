# Challenge 02: RBAC 引擎

## 描述
实现完整的 RBAC 权限引擎

## TODO
1. create_role(name) 创建角色
2. assign_role(user, role) / revoke_role(user, role)
3. check(user, resource, action) → bool
4. get_user_permissions(user) → Set[Permission]
5. 多角色权限合并

## 约束
- 纯 Python，不使用第三方权限库
- 所有公开方法需类型标注
- 异常使用自定义的 PermissionDenied
