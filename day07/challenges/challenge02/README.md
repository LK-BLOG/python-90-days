# 挑战2：Todo管理器

## 项目名称
Todo管理器实现

## 目标
实现Todo管理器类，提供完整的CRUD操作和数据持久化功能。

## 背景
管理器是Todo系统的核心，负责所有Todo的增删改查操作。

## 功能要求
1. **数据持久化**：
   - JSON文件存储
   - 自动保存和加载
   - 错误处理

2. **CRUD操作**：
   - 添加Todo
   - 删除Todo
   - 编辑Todo
   - 查询Todo

3. **高级功能**：
   - 搜索Todo
   - 过滤Todo（按优先级、状态）
   - 统计信息

## 输入/输出示例
```python
# 创建管理器
manager = TodoManager("todos.json")

# 添加Todo
todo = manager.add_todo("学习Python", priority="高")
print(f"添加成功，ID: {todo['id']}")

# 搜索Todo
results = manager.search_todos("Python")
print(f"找到 {len(results)} 个匹配的Todo")

# 统计信息
stats = manager.get_statistics()
print(f"总数: {stats['总数']}")
```

## 限制条件
1. 仅使用标准库
2. 必须处理所有异常
3. 数据必须持久化
4. 代码必须有中文注释

## 验收标准
- [ ] 数据保存和加载正常
- [ ] CRUD操作正常
- [ ] 搜索功能正常
- [ ] 统计功能正常
- [ ] 异常处理完善
- [ ] 通过所有测试

## 难度评级
⭐⭐⭐☆☆ (3/5)
