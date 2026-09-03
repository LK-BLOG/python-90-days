# Challenge 03: 权限装饰器

## 描述
实现 @require 装饰器

## TODO
1. @require(resource, action) 单权限检查
2. @require_any(resource1=action1, ...) 多权限OR检查
3. 权限不足抛 PermissionDenied
4. 每次调用记录审计日志

## 约束
- 纯 Python，不使用第三方权限库
- 所有公开方法需类型标注
- 异常使用自定义的 PermissionDenied
