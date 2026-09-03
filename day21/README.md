# Day 21: 装饰器

## 今日概览
| 项目 | 内容 |
|------|------|
| **主题** | 装饰器原理、带参装饰器、类装饰器、实用装饰器 |
| **难度** | ⭐⭐⭐⭐ 中高级 |
| **前置知识** | Day 19-20（迭代器/生成器）、Day 17（闭包） |
| **预计时间** | 4-5 小时 |

## 学习目标
  - 理解闭包 -> 装饰器的演进路径
  - 编写无参/带参装饰器，掌握 functools.wraps
  - 理解类装饰器与装饰器叠加顺序
  - 掌握 property/staticmethod/classmethod
  - 构建实用装饰器（@timer/@debug/@retry/@cache/@validate）

## 文件结构
```
day21/
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
4. 挑战 challenges/day21/ 下的5个关卡
5. Boss战: HTTP请求装饰器系统（@rate_limit/@cache/@retry/@log/@authenticate，可叠加）