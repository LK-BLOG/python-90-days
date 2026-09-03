# Day 20: 生成器

## 今日概览
| 项目 | 内容 |
|------|------|
| **主题** | yield、生成器管道、协程基础、itertools进阶 |
| **难度** | ⭐⭐⭐ 中级进阶 |
| **前置知识** | Day 19（迭代器协议） |
| **预计时间** | 3-4 小时 |

## 学习目标
  - 掌握 yield 基础与生成器本质（就是迭代器）
  - 理解 yield 表达式（send）与协程基础
  - 使用 yield from 实现委托生成器
  - 对比生成器表达式 vs 列表推导式
  - 构建生成器管道处理流式数据

## 文件结构
```
day20/
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
4. 挑战 challenges/day20/ 下的5个关卡
5. Boss战: ETL数据管道（用生成器链处理CSV/JSON数据，支持数据清洗、转换、聚合、输出）