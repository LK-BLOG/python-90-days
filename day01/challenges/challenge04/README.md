# 挑战四：参数验证器

## 难度
★★★★☆

## 目标
实现参数验证系统，验证函数参数的类型和值范围。

## 功能要求
1. 定义验证规则：类型、范围、必填/可选
2. 实现 `validate(func, rules, *args, **kwargs)`
3. 验证通过调用原函数，失败返回错误列表

## 示例
```python
rules = {"name": {"type": str, "min_length": 2}, "age": {"type": int, "min": 0, "max": 150}}
validate(create_user, rules, "张", age=25, email="a@b.com")
# "Error: name长度不能小于2"
```

## 验收标准
1. ✅ 类型验证正确
2. ✅ 范围验证正确
3. ✅ 字符串长度验证
4. ✅ 返回有意义的错误信息
5. ✅ 验证通过正常执行函数
