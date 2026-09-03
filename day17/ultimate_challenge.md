# Day 17 Boss 挑战 — 配置管理系统

## 项目名称
ConfigManager — 多级配置系统

## 目标
设计一个配置管理系统，支持多级配置、环境覆盖、验证、JSON/TOML 序列化。

## 功能要求

### 配置类
1. ServerConfig: host, port, timeout
2. DatabaseConfig: url, pool_size, echo
3. AppConfig: server, database, debug, log_level

### 验证
4. port 范围 1-65535
5. pool_size >= 1
6. log_level 枚举值

### 环境覆盖
7. 环境变量覆盖配置: APP_SERVER__PORT=8080
8. .env 文件支持

### 序列化
9. to_dict(), from_dict()
10. to_json(), from_json()
11. to_toml(), from_toml()

### 配置管理器
12. ConfigManager 类
13. load(path) 从文件加载
14. save(path) 保存到文件
15. override(key, value) 覆盖单个值
16. merge(other) 合并配置

## 验收标准
- AppConfig(server=ServerConfig(port=8080)) 正常创建
- 端口超范围抛 ValueError
- 环境变量可以覆盖配置
- 配置可以序列化为 JSON 和 TOML
- ConfigManager 可以加载和保存配置文件
