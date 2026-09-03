# Boss 挑战: EventEmitter 事件系统

## 目标
设计完整的事件系统，综合运用 Day 13 知识

## 核心功能
- on/emit/off/once 基础事件
- Event 描述符（支持 += 操作）
- 事件命名空间（点号分隔）
- 事件优先级
- 错误隔离

## 验收标准
1. on/emit/off 正确工作
2. once 只触发一次
3. Event 描述符支持 += 操作
4. handler 异常不影响其他
5. 事件统计功能正常
