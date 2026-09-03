# Challenge 01: 基础权限对象

## 描述
实现 Permission 和 Role 数据类

## TODO
1. 实现 Permission.__eq__ 和 __hash__
2. 实现 Role.add_permission() 和 remove_permission()
3. 实现 Role.has_permission()（考虑 MANAGE 覆盖同资源子操作）
4. 测试：创建角色、添加权限、检查权限

## 约束
- 纯 Python，不使用第三方权限库
- 所有公开方法需类型标注
- 异常使用自定义的 PermissionDenied
