# 挑战三：函数调度器

## 难度
★★★☆☆

## 目标
实现一个函数调度器，根据参数中的 action 值调用对应操作。

## 功能要求
1. 实现 `register(action, func)` 注册操作
2. 实现 `dispatch(action, **params)` 调用操作
3. 未注册的 action 返回错误信息
4. 支持覆盖已注册的 action
5. 可列出所有已注册的 action

## 示例
```python
d = Dispatcher()
d.register("add", lambda a, b: a + b)
d.dispatch("add", a=3, b=5)      # 8
d.dispatch("unknown")             # "Error: unknown action"
```

## 验收标准
1. ✅ 注册和调用正常
2. ✅ 参数正确传递
3. ✅ 未注册action返回错误
4. ✅ 可覆盖注册
5. ✅ 可列出所有action
