# Challenge 04: 权限继承

## 描述
实现角色继承（Role Hierarchy）

## TODO
1. Role 支持 parent 参数继承父角色权限
2. get_effective_permissions(role) 返回含继承的全部权限
3. 检测循环继承并报错
4. 子角色可覆盖父角色的特定权限

## 约束
- 纯 Python，不使用第三方权限库
- 所有公开方法需类型标注
- 异常使用自定义的 PermissionDenied
