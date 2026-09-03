# Day 9 挑战：JSON数据处理

## 挑战概述
掌握JSON数据处理，实现数据序列化和验证。

## 核心挑战
1. **JSON基础操作**：序列化/反序列化
2. **自定义编解码器**：处理特殊数据类型
3. **数据验证**：确保数据格式正确
4. **配置文件管理**：JSON配置读写

## 具体任务

### 挑战1：自定义JSON编解码器
实现支持特殊类型的JSON编解码器：
- 日期时间处理
- 集合处理
- Decimal处理
- 自定义对象处理

**要求**：
- 继承json.JSONEncoder
- 实现object_hook
- 处理嵌套结构

### 挑战2：JSON数据验证器
实现JSON数据验证：
- 类型检查
- 范围验证
- 格式验证
- 自定义规则

**要求**：
- 支持多种验证规则
- 提供详细的错误信息
- 支持嵌套验证

### 挑战3：配置文件管理器
实现JSON配置文件管理：
- 读取配置
- 修改配置
- 保存配置
- 默认值处理

**要求**：
- 支持嵌套配置
- 验证配置格式
- 保持注释（如果可能）

## 输入/输出示例
```python
# 自定义编码器
encoder = CustomEncoder()
data = {"date": datetime.now(), "tags": {"a", "b"}}
json_str = encoder.encode(data)
print(json_str)

# 数据验证
validator = JSONValidator(schema)
result = validator.validate(data)
print(result)
```

## 限制条件
1. 仅使用标准库
2. 必须处理所有异常
3. 代码必须有中文注释

## 验收标准
- [ ] JSON序列化正常
- [ ] 自定义类型处理正确
- [ ] 数据验证有效
- [ ] 配置文件管理正常
- [ ] 通过所有测试

## 难度评级
⭐⭐⭐☆☆ (3/5)
