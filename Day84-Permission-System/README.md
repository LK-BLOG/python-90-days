# Day 84: Permission System (权限系统)

## 学习目标
- 理解 RBAC（基于角色的访问控制）权限模型
- 实现工具调用权限控制
- 掌握用户权限验证流程
- 学会设计审计日志系统

## 核心概念
1. **权限基础**：权限 = 主体 + 动作 + 资源
2. **RBAC模型**：用户 → 角色 → 权限，三层映射
3. **装饰器权限检查**：用 Python 装饰器优雅地做权限校验
4. **审计日志**：谁在什么时间对什么资源做了什么操作

## 文件结构
```
Day84-Permission-System/
├── README.md                    # 本文件
├── lesson.md                    # 详细课程内容
├── challenge.md                 # 挑战说明
├── ultimate_challenge.md        # 终极挑战说明
├── examples/                    # 示例代码
│   ├── 01_rbac_model.py
│   ├── 02_permission_decorator.py
│   └── 03_audit_logger.py
├── starter/                     # 起步代码
│   └── permission_system.py
├── tests/                       # 测试
│   └── test_permission.py
└── challenges/
    └── day84/
        ├── challenge01-05/      # 5个小挑战
        └── ultimate/            # 终极挑战
```

## 预备知识
- Python 装饰器
- 数据类 (dataclass)
- 枚举 (enum)
- 基本的设计模式

## 预计学习时间
- 课程阅读：2 小时
- 示例实践：1.5 小时
- 挑战练习：2-3 小时
- 终极挑战：3-4 小时
