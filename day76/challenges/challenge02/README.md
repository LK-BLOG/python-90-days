# Day 76 - 挑战 2: 工具注册系统
## 难度: ⭐⭐

## 任务
实现一个工具注册表（ToolRegistry）。

## 要求
1. egister(name, tool): 注册工具
2. get(name): 按名称获取工具
3. list_tools(): 列出所有工具
4. get_descriptions(): 生成 LLM 可用的工具描述
5. xecute(name, **kwargs): 查找并执行工具
