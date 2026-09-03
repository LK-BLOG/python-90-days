# Challenge 05: 策略引擎

## 描述
实现简单 ABAC 策略引擎

## TODO
1. PolicyRule 类，支持条件表达式评估
2. 条件格式：attr op value（如 department == engineering）
3. 策略优先级：explicit deny > allow > default deny
4. 与 RBAC 组合使用

## 约束
- 纯 Python，不使用第三方权限库
- 所有公开方法需类型标注
- 异常使用自定义的 PermissionDenied
