# Day 13 Boss 挑战 — 事件系统 EventEmitter

## 项目名称
EventEmitter — 轻量级事件系统

## 背景
事件驱动是现代软件的核心模式。Node.js、浏览器 DOM、Qt 都用 EventEmitter。
本挑战让你从零实现一个完整的事件系统，综合运用 Day 13 所有知识。

## 目标
设计一个 EventEmitter 类，支持事件的注册、触发、移除，并用描述符管理事件定义。

## 功能要求

### 基础事件
1. `on(event, callback)` — 注册事件监听
2. `once(event, callback)` — 只触发一次
3. `emit(event, *args, **kwargs)` — 触发事件
4. `off(event, callback)` — 移除监听
5. `listeners(event)` — 返回事件监听列表

### 事件描述符
6. 创建 `Event` 描述符类
7. 类属性声明: `click = Event('click')`
8. 支持 `obj.click += handler`（注册）
9. 支持 `obj.click -= handler`（移除）
10. 支持 `obj.click.emit(data)`（触发）

### 事件组/命名空间
11. `EventGroup` 类，批量注册多个事件
12. 命名空间: `obj.on('user.login', handler)` 支持点号分隔

### 高级特性
13. 事件优先级（priority 参数）
14. 错误处理（某个 handler 出错不影响其他）
15. 用类属性追踪所有实例的事件统计

## 输入输出示例

```python
em = EventEmitter()

# 基础用法
em.on('data', lambda x: print(f'received: {x}'))
em.emit('data', 'hello')  # received: hello

# once
counter = [0]
def inc():
    counter[0] += 1
em.once('tick', inc)
em.emit('tick')
em.emit('tick')  # 不会再触发
print(counter[0])  # 1

# 描述符
class Button(EventEmitter):
    click = Event('click')
    hover = Event('hover')

btn = Button()
btn.on('click', lambda: print('clicked'))
btn.click.emit()  # clicked
btn.click += lambda: print('clicked again')
btn.click.emit()
# clicked
# clicked again
```

## 验收标准
1. 基础 on/emit/off/once 正确工作
2. Event 描述符支持 += 操作
3. 多个 handler 按注册顺序触发
4. off 正确移除指定 handler
5. once 只触发一次
6. 错误隔离（handler 异常不影响其他）
7. 事件统计功能正常

## 可选扩展
- 异步事件支持 (async/await)
- 事件通配符 (`user.*`)
- 内存泄漏检测（长时间未触发的事件）
- 事件日志记录器
