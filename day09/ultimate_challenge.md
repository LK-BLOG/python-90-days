# Day 9 Boss挑战：通用数据迁移工具

## 挑战描述
实现一个通用数据迁移工具，支持JSON、CSV、XML格式互转，并带数据验证。

## 核心功能
1. **格式转换**：JSON ↔ CSV ↔ XML
2. **数据验证**：确保数据格式正确
3. **迁移报告**：记录迁移过程
4. **错误处理**：优雅的错误恢复

## 具体任务

### 任务1：格式检测
自动检测数据格式：
- 检测JSON格式
- 检测CSV格式
- 检测XML格式
- 处理未知格式

### 任务2：JSON转换
实现JSON与其他格式互转：
- JSON转CSV
- JSON转XML
- CSV转JSON
- XML转JSON

### 任务3：数据验证
验证数据完整性：
- 字段验证
- 类型检查
- 格式验证
- 重复检测

### 任务4：迁移报告
生成迁移报告：
- 转换统计
- 错误记录
- 性能分析
- 日志记录

## 输入/输出示例
```python
# 创建迁移工具
migrator = DataMigrator()

# JSON转CSV
migrator.convert("data.json", "data.csv")

# CSV转JSON
migrator.convert("data.csv", "data.json")

# 带验证的转换
migrator.convert("input.json", "output.csv", validate=True)
```

## 限制条件
1. 仅使用标准库
2. 必须处理大文件
3. 代码必须有详细注释

## 验收标准
- [ ] 格式检测正确
- [ ] 格式转换正常
- [ ] 数据验证有效
- [ ] 迁移报告完整
- [ ] 通过所有测试

## 难度评级
⭐⭐⭐⭐☆ (4/5)
