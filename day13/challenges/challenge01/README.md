# Challenge 1: 学生计数器

## 目标
用类属性实现自动计数的 Student 类

## 功能要求
1. 类属性 `total_count` 追踪学生数量
2. 每次创建实例 +1
3. `__del__` 中 -1
4. 实例属性: name, age, scores
5. 方法: average_score()

## 验收标准
- Student.total_count 初始为 0
- 创建 Student 后 count +1
- del 实例后 count -1
- average_score() 返回正确平均分
