# Day 14 挑战 — 继承体系

## Challenge 1: 图形继承链
**目标**: 用 ABC 设计 Shape 继承体系

**要求**:
1. Shape 抽象基类（area, perimeter 抽象方法）
2. Circle, Rectangle, Triangle 继承 Shape
3. 每个子类实现面积和周长计算
4. 支持 `__eq__` 比较面积

## Challenge 2: MRO 分析器
**目标**: 理解 C3 MRO

**要求**:
1. 创建复杂的多继承层次
2. 分析方法调用顺序
3. 验证 super() 的行为

## Challenge 3: Mixin 工具箱
**目标**: 用 Mixin 给类添加功能

**要求**:
1. JsonMixin: to_json/from_json
2. HashMixin: 自动生成 __hash__
3. CloneMixin: 深拷贝功能

## Challenge 4: 接口检查系统
**目标**: 实现鸭子类型检查

**要求**:
1. 用 ABC 定义接口
2. 用 issubclass 检查
3. 用 Protocol 做结构化子类型

## Challenge 5: 钻石继承调试
**目标**: 理解并解决钻石继承问题

**要求**:
1. 实现钻石继承
2. 分析 MRO
3. 用 super() 避免重复调用
