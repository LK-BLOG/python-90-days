# 挑战二：配置合并器

## 难度
★★☆☆☆

## 目标
实现智能的配置合并函数，支持深度合并和覆盖策略。

## 功能要求
实现 `merge_configs(defaults, user_config, override_mode="replace")`：
- "replace"：用户配置完全替换默认配置中的同名键
- "extend"：列表合并（拼接），字典递归合并
- 返回合并后的新配置（不修改原始数据）

## 示例
```python
defaults = {"db": {"host": "localhost", "port": 3306}, "features": ["auth"]}
user = {"db": {"port": 5432, "name": "mydb"}, "features": ["cache"]}

merge_configs(defaults, user, "replace")
# {"db": {"port": 5432, "name": "mydb"}, "features": ["cache"]}

merge_configs(defaults, user, "extend")
# {"db": {"host": "localhost", "port": 5432, "name": "mydb"}, "features": ["auth", "cache"]}
```

## 验收标准
1. ✅ replace模式正确覆盖
2. ✅ extend模式合并列表
3. ✅ 嵌套字典递归合并
4. ✅ 不修改原始字典
