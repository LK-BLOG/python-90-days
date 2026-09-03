# Day 12 Boss挑战：CLI Todo包重构

## 挑战描述
将Day 7的CLI Todo系统重构为标准Python包，支持pip install -e . 安装。

## 核心功能
1. **标准包结构**：符合Python包标准
2. **可安装**：支持pip install
3. **命令行接口**：提供CLI工具
4. **完整文档**：README和docstrings

## 具体任务

### 任务1：包结构重构
将Todo系统重构为包：
- 创建包目录结构
- 拆分模块
- 添加__init__.py
- 配置包元数据

### 任务2：CLI接口
实现命令行接口：
- 使用argparse或click
- 支持各种命令
- 参数验证
- 帮助信息

### 任务3：打包配置
配置包发布：
- 创建pyproject.toml
- 添加依赖声明
- 配置入口点
- 编写README

### 任务4：测试和文档
完善测试和文档：
- 单元测试
- 集成测试
- 用户文档
- API文档

## 输入/输出示例
```bash
# 安装包
pip install -e .

# 使用CLI
todo add "学习包开发" --priority high
todo list
todo complete 1

# 在代码中使用
from todo_cli import TodoManager
manager = TodoManager()
manager.add("学习包开发")
```

## 包结构
```
todo-cli/
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       ├── models.py
│       ├── storage.py
│       ├── manager.py
│       └── cli.py
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

## 限制条件
1. 符合Python包标准
2. 支持pip install
3. 提供CLI接口
4. 代码必须有详细注释

## 验收标准
- [ ] 包结构正确
- [ ] 可以pip install
- [ ] CLI功能正常
- [ ] 文档完整
- [ ] 通过所有测试

## 难度评级
⭐⭐⭐⭐☆ (4/5)
