# Day 23: 类型系统

## 今日概览
| 项目 | 内容 |
|------|------|
| **主题** | Type Hints、泛型、Protocol、TypedDict、mypy |
| **难度** | ⭐⭐⭐⭐ 中高级 |
| **前置知识** | Day 1-22 全部内容 |
| **预计时间** | 3-4 小时 |

## 学习目标
  - 掌握 type hints 基础（函数注解、变量注解）
  - 理解内置类型标注 list[dict[str, int]]
  - 使用 Optional/Union/Type 复合类型
  - 掌握 TypeVar 泛型与 Protocol 结构子类型
  - 使用 TypedDict 和类型安全设计模式

## 文件结构
```
day23/
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
4. 挑战 challenges/day23/ 下的5个关卡
5. Boss战: 给RPG项目添加完整类型注解，编写类型安全的API接口