# Day 22: 上下文管理器

## 今日概览
| 项目 | 内容 |
|------|------|
| **主题** | with协议、contextlib、资源管理、事务控制 |
| **难度** | ⭐⭐⭐⭐ 中高级 |
| **前置知识** | Day 21（装饰器）、Day 17（闭包） |
| **预计时间** | 3-4 小时 |

## 学习目标
  - 掌握 __enter__/__exit__ 协议
  - 使用 contextmanager 装饰器快速创建上下文管理器
  - 理解 ExitStack 动态管理资源
  - 结合装饰器构建资源管理中间件
  - 实现数据库连接池、事务管理、临时环境

## 文件结构
```
day22/
  README.md              # 本文件
  lesson.md              # 详细课程
  challenge.md           # 挑战说明
  ultimate_challenge.md  # Boss挑战
  examples/              # 示例代码
  starter/               # 练习起步代码
  tests/                 # 测试用例
```

## 学习路线
1. 先读 lesson.md
2. 运行 examples/ 下的示例
3. 完成 starter/ 中的练习
4. 挑战 challenges/day22/ 下的5个关卡
5. Boss战: 资源管理中间件（数据库连接池 + 日志上下文 + 计时器 + 重试）