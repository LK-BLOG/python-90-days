# Day 19: 迭代器

## 今日概览
| 项目 | 内容 |
|------|------|
| **主题** | 迭代器协议、自定义迭代器、itertools |
| **难度** | ⭐⭐⭐ 中级进阶 |
| **前置知识** | Day 1-18（OOP、魔术方法、数据结构） |
| **预计时间** | 3-4 小时 |

## 学习目标
  - 理解可迭代对象 vs 迭代器的本质区别
  - 掌握 __iter__ / __next__ / StopIteration 协议
  - 编写自定义迭代器类（有限/无限）
  - 熟练使用 itertools 常用工具函数
  - 理解迭代器的内存优势（惰性求值）

## 文件结构
```
day19/
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
4. 挑战 challenges/day19/ 下的5个关卡
5. Boss战: 大数据文件流式处理器（逐行读取GB级日志，支持过滤/聚合/分组，内存恒定）