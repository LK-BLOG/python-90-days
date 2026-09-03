# Challenge 04: 配置文件解析器

## 项目名称：ConfigFlow

## 目标
编写一个配置管理器，支持多来源配置合并。

## 功能要求

### 1. 多格式支持
- 支持 pyproject.toml
- 支持 .env 文件
- 支持 YAML（可选）
- 支持 JSON（可选）

### 2. 配置合并
- 环境变量 > .env > 配置文件 > 默认值
- 支持配置覆盖
- 支持配置命名空间

### 3. 配置验证
- 类型检查
- 必填字段验证
- 自定义验证规则

### 4. 配置访问
- 点号访问：config.database.host
- 默认值：config.get("key", default)
- 配置迭代

## 输入
- 配置文件路径
- 环境变量前缀

## 输出
- 配置对象（支持属性访问）
- 配置验证结果

## 限制
- 类型安全
- 线程安全
- 支持热重载

## 示例
```python
from configflow import Config

config = Config(
    config_file="pyproject.toml",
    env_prefix="MYAPP_"
)

# 点号访问
db_host = config.database.host

# 带默认值
debug = config.get("debug", False)

# 配置验证
config.validate(required=["database.host", "database.port"])
```

## 验收标准
- [ ] 支持 pyproject.toml 解析
- [ ] 支持 .env 文件
- [ ] 环境变量覆盖
- [ ] 配置验证
- [ ] 点号访问语法

## 可选扩展
- 支持配置加密
- 支持配置版本管理
- 支持配置变更通知
- 支持远程配置（Consul、etcd）
